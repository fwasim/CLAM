import pdb
import os
import pandas as pd
from datasets.dataset_generic import Generic_WSI_Classification_Dataset, Generic_MIL_Dataset, save_splits
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Creating splits for whole slide classification')
parser.add_argument('--label_frac', type=float, default= 1.0,
                    help='fraction of labels (default: 1)')
parser.add_argument('--seed', type=int, default=1,
                    help='random seed (default: 1)')
parser.add_argument('--k', type=int, default=10,
                    help='number of splits (default: 10)')
parser.add_argument('--task', type=str, choices=['task_1_tumor_vs_normal', 'task_2_tumor_subtyping'])
parser.add_argument('--val_frac', type=float, default= 0.1,
                    help='fraction of labels for validation (default: 0.1)')
parser.add_argument('--test_frac', type=float, default= 0.1,
                    help='fraction of labels for test (default: 0.1)')

parser.add_argument('--data_dir', type=str, default='./',
                    help='directory relative to current path that contains the data used for filtering excel file (default: ./)')

parser.add_argument('--csv_dir', type=str, default='./',
                    help='path to csv file containing dataset info (default: ./)')

parser.add_argument('--label_col', type=str, default='label',
                    help='name of the column holding the labels (default: \'label\')')

args = parser.parse_args()

# Reading the data from input directory and prepping the filter such that only those data are taken in training/testing
print('==========================================================')
image_list = os.listdir(str(os.getcwd()) + '/' + args.data_dir)
image_list = list(map(lambda a : int(a.split('.')[0]), image_list))

if args.data_dir[-1] == '/':
    args.data_dir = args.data_dir[:-1]

print('Number of images in \'' + args.data_dir.split('/')[-1] + '\': ' + str(len(image_list)))

label_dict = {6:0, 7:1}

print('\n*****************************************************')
print('Label mapping dictionary. Check if this is correct!\n')
print(str(label_dict))
print('******************************************************\n')

if args.task == 'task_1_tumor_vs_normal':
    args.n_classes=2
    dataset = Generic_WSI_Classification_Dataset(csv_path = 'dataset_csv/tumor_vs_normal_dummy_clean.csv',
                            shuffle = False, 
                            seed = args.seed, 
                            print_info = True,
                            label_dict = label_dict,
                            filter_dict = {'slide_id':image_list},
                            patient_strat=True,
                            ignore=[])

elif args.task == 'task_2_tumor_subtyping':
    args.n_classes=2
    dataset = Generic_WSI_Classification_Dataset(csv_path = args.csv_dir,
                            shuffle = False, 
                            seed = args.seed, 
                            print_info = True,
                            label_dict = label_dict,
                            filter_dict = {'slide_id':image_list},
                            patient_strat= True,
                            patient_voting='maj',
                            ignore=[],
                            label_col = 'encoded Sublabel')

else:
    raise NotImplementedError

num_slides_cls = np.array([len(cls_ids) for cls_ids in dataset.patient_cls_ids])
val_num = np.round(num_slides_cls * args.val_frac).astype(int)
test_num = np.round(num_slides_cls * args.test_frac).astype(int)

if __name__ == '__main__':
    if args.label_frac > 0:
        label_fracs = [args.label_frac]
    else:
        label_fracs = [0.1, 0.25, 0.5, 0.75, 1.0]
    
    for lf in label_fracs:
        split_dir = 'splits/'+ str(args.task) + '_{}'.format(int(lf * 100))
        os.makedirs(split_dir, exist_ok=True)
        dataset.create_splits(k = args.k, val_num = val_num, test_num = test_num, label_frac=lf)
        for i in range(args.k):
            dataset.set_splits()
            descriptor_df = dataset.test_split_gen(return_descriptor=True)
            splits = dataset.return_splits(from_id=True)
            save_splits(splits, ['train', 'val', 'test'], os.path.join(split_dir, 'splits_{}.csv'.format(i)))
            save_splits(splits, ['train', 'val', 'test'], os.path.join(split_dir, 'splits_{}_bool.csv'.format(i)), boolean_style=True)
            descriptor_df.to_csv(os.path.join(split_dir, 'splits_{}_descriptor.csv'.format(i)))