import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
from models.model_mil import MIL_fc, MIL_fc_mc
from models.model_clam import CLAM_SB, CLAM_MB
import pdb
import os
import pandas as pd
from utils.utils import *
from utils.core_utils import Accuracy_Logger
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def initiate_model(args, ckpt_path):
    print('Init Model')    
    model_dict = {"dropout": args.drop_out, 'n_classes': args.n_classes}
    
    if args.model_size is not None and args.model_type in ['clam_sb', 'clam_mb']:
        model_dict.update({"size_arg": args.model_size})
    
    if args.model_type =='clam_sb':
        model = CLAM_SB(**model_dict)
    elif args.model_type =='clam_mb':
        model = CLAM_MB(**model_dict)
    else: # args.model_type == 'mil'
        if args.n_classes > 2:
            model = MIL_fc_mc(**model_dict)
        else:
            model = MIL_fc(**model_dict)

    print_network(model)

    ckpt = torch.load(ckpt_path)
    ckpt_clean = {}
    for key in ckpt.keys():
        if 'instance_loss_fn' in key:
            continue
        ckpt_clean.update({key.replace('.module', ''):ckpt[key]})
    model.load_state_dict(ckpt_clean, strict=True)

    model.relocate()
    model.eval()
    return model

def eval(dataset, args, ckpt_path):
    model = initiate_model(args, ckpt_path)
    
    print('Init Loaders')
    loader = get_simple_loader(dataset)
    print("Checkpoint path: " + str(ckpt_path))
    fold_no = ckpt_path.split("/")[-1].split("_")[1]
    patient_results, test_error, auc, df, _ = summary(model, loader, args, fold_no)
    print('test_error: ', test_error)
    print('auc: ', auc)
    return model, patient_results, test_error, auc, df


def compute_class_metrics(all_labels, all_preds, n_classes):
    metrics = {'TP': [], 'TN': [], 'FP': [], 'FN': []}

    for c in range(n_classes):
        tp = np.sum((all_labels == c) & (all_preds == c))
        tn = np.sum((all_labels != c) & (all_preds != c))
        fp = np.sum((all_labels != c) & (all_preds == c))
        fn = np.sum((all_labels == c) & (all_preds != c))
        
        metrics['TP'].append(tp)
        metrics['TN'].append(tn)
        metrics['FP'].append(fp)
        metrics['FN'].append(fn)

    return metrics

def compute_class_metrics_percentage(all_labels, all_preds, n_classes):
    metrics = {'TP (%)': [], 'TN (%)': [], 'FP (%)': [], 'FN (%)': []}

    for c in range(n_classes):
        tp = np.sum((all_labels == c) & (all_preds == c))
        tn = np.sum((all_labels != c) & (all_preds != c))
        fp = np.sum((all_labels != c) & (all_preds == c))
        fn = np.sum((all_labels == c) & (all_preds != c))
        
        total_actual_positives = np.sum(all_labels == c)
        total_actual_negatives = np.sum(all_labels != c)
        
        metrics['TP (%)'].append((tp / total_actual_positives if total_actual_positives != 0 else 0) * 100)
        metrics['TN (%)'].append((tn / total_actual_negatives if total_actual_negatives != 0 else 0) * 100)
        metrics['FP (%)'].append((fp / total_actual_negatives if total_actual_negatives != 0 else 0) * 100)
        metrics['FN (%)'].append((fn / total_actual_positives if total_actual_positives != 0 else 0) * 100)

    return metrics

def summary(model, loader, args, fold_no):
    print("Fold no: " + str(fold_no))
    acc_logger = Accuracy_Logger(n_classes=args.n_classes)
    model.eval()
    test_loss = 0.
    test_error = 0.

    all_probs = np.zeros((len(loader), args.n_classes))
    all_labels = np.zeros(len(loader))
    all_preds = np.zeros(len(loader))

    slide_ids = loader.dataset.slide_data['slide_id']
    patient_results = {}
    for batch_idx, (data, label) in enumerate(loader):
        data, label = data.to(device), label.to(device)
        slide_id = slide_ids.iloc[batch_idx]
        with torch.no_grad():
            logits, Y_prob, Y_hat, _, results_dict = model(data)
        
        acc_logger.log(Y_hat, label)
        
        probs = Y_prob.cpu().numpy()

        all_probs[batch_idx] = probs
        all_labels[batch_idx] = label.item()
        all_preds[batch_idx] = Y_hat.item()

        patient_results.update({slide_id: {'slide_id': np.array(slide_id), 'prob': probs, 'label': label.item()}})
        
        error = calculate_error(Y_hat, label)
        test_error += error

    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('./confusion_matrix'+str(fold_no)+'.png')
    plt.close()
    
    class_metrics = compute_class_metrics(all_labels, all_preds, args.n_classes)
    # Create DataFrame for visualization
    df_metrics = pd.DataFrame(class_metrics)

    # Plotting
    plt.figure(figsize=(10, 7))
    sns.heatmap(df_metrics, annot=True, cmap='Blues', fmt='g', linewidths=.5)
    plt.title('Metrics for Each Class')
    plt.yticks(rotation=0)  # Keeps the class labels horizontal
    plt.savefig('./metrics_table' + str(fold_no) + '.png')
    plt.close()

    class_metrics = compute_class_metrics_percentage(all_labels, all_preds, args.n_classes)
    # Create DataFrame for visualization
    df_metrics = pd.DataFrame(class_metrics)

    # Plotting
    plt.figure(figsize=(10, 7))
    sns.heatmap(df_metrics, annot=True, cmap='Blues', fmt='.2f', linewidths=.5)
    plt.title('Metrics for Each Class (in Percentage)')
    plt.yticks(rotation=0)  # Keeps the class labels horizontal
    plt.savefig('./metrics_table_percentage' + str(fold_no) + '.png')
    plt.close()


    del data
    test_error /= len(loader)

    aucs = []
    if len(np.unique(all_labels)) == 1:
        auc_score = -1

    else: 
        if args.n_classes == 2:
            auc_score = roc_auc_score(all_labels, all_probs[:, 1])
        else:
            binary_labels = label_binarize(all_labels, classes=[i for i in range(args.n_classes)])
            for class_idx in range(args.n_classes):
                if class_idx in all_labels:
                    fpr, tpr, _ = roc_curve(binary_labels[:, class_idx], all_probs[:, class_idx])
                    aucs.append(auc(fpr, tpr))
                else:
                    aucs.append(float('nan'))
            if args.micro_average:
                binary_labels = label_binarize(all_labels, classes=[i for i in range(args.n_classes)])
                fpr, tpr, _ = roc_curve(binary_labels.ravel(), all_probs.ravel())
                auc_score = auc(fpr, tpr)
            else:
                auc_score = np.nanmean(np.array(aucs))

    results_dict = {'slide_id': slide_ids, 'Y': all_labels, 'Y_hat': all_preds}
    for c in range(args.n_classes):
        results_dict.update({'p_{}'.format(c): all_probs[:,c]})
    df = pd.DataFrame(results_dict)
    return patient_results, test_error, auc_score, df, acc_logger