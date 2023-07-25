from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil

# This file takes all the feature vectors of all images, refers to the excel file containing the labels
# and copies those feature vector files over to their appropriate folder

PATH_TO_EXCEL_FILE = '/scratch/d/dsussman/fawasim/dataset_images_100_percent.xlsx'
FEATURES_DIR = '/scratch/d/dsussman/fawasim/Image_features'
FEATURES_DIR_H5 = FEATURES_DIR + '/h5_files'
FEATURES_DIR_PT = FEATURES_DIR + '/pt_files'
DEST_DIR = '/scratch/d/dsussman/fawasim/Output'
DEST_DIR_BENIGN = DEST_DIR + '/Benign'
DEST_DIR_BENIGN_H5 = DEST_DIR_BENIGN + '/FEATURES_DIRECTORY_MATTHEW/h5_files/'
DEST_DIR_BENIGN_PT = DEST_DIR_BENIGN + '/FEATURES_DIRECTORY_MATTHEW/pt_files/'
DEST_DIR_CANCER = DEST_DIR + '/Cancer'
DEST_DIR_CANCER_H5 = DEST_DIR_CANCER + '/FEATURES_DIRECTORY_MATTHEW/h5_files/'
DEST_DIR_CANCER_PT = DEST_DIR_CANCER + '/FEATURES_DIRECTORY_MATTHEW/pt_files/'
DEST_DIR_HYPERPLASIA = DEST_DIR + '/Hyperplasia'
DEST_DIR_HYPERPLASIA_H5 = DEST_DIR_HYPERPLASIA + '/FEATURES_DIRECTORY_MATTHEW/h5_files/'
DEST_DIR_HYPERPLASIA_PT = DEST_DIR_HYPERPLASIA + '/FEATURES_DIRECTORY_MATTHEW/pt_files/'

onlyfiles = [f for f in listdir(FEATURES_DIR_H5) if isfile(join(FEATURES_DIR_H5, f))]
print("\nNo. of files in source directory:")
print(str(len(onlyfiles)))

df = pd.read_excel(PATH_TO_EXCEL_FILE)
print('\nThis is how the excel file looks like:\n')
print(df.head())

print('\nHow many labels are there:\n')
print(df['Label'].value_counts())
ids = list(df['Participant ID'])

excluded_df = pd.DataFrame(columns=df.columns)

for i in onlyfiles:
    file_name = int(i.split('.')[0])
    test_df = df[df['Participant ID'] == file_name]

    if test_df.shape[0] == 1:
        label = test_df["Label"].values[0]

        if label == 'Benign':
            print("Copying file " + FEATURES_DIR_H5 + '/' + i + " to " + DEST_DIR_BENIGN_H5 + i)
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_BENIGN_H5 + i)
            shutil.copyfile(FEATURES_DIR_PT + '/' + str(file_name) + '.pt', DEST_DIR_BENIGN_PT + str(file_name) + '.pt')
        elif label == 'Neoplasia':
            print("Copying file " + FEATURES_DIR_H5 + '/' + i + " to " + DEST_DIR_CANCER_H5 + i)
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_CANCER_H5 + i)
            shutil.copyfile(FEATURES_DIR_PT + '/' + str(file_name) + '.pt', DEST_DIR_CANCER_PT + str(file_name) + '.pt')
        else:
            print("Copying file " + FEATURES_DIR_H5 + '/' + i + " to " + DEST_DIR_HYPERPLASIA_H5 + i)
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_HYPERPLASIA_H5 + i)
            shutil.copyfile(FEATURES_DIR_PT + '/' + str(file_name) + '.pt', DEST_DIR_HYPERPLASIA_PT + str(file_name) + '.pt')
    else:
        if excluded_df.empty:
            excluded_df = test_df
        else:
            excluded_df.append(df)

print("\nNo. of Benign files copied:")
print("h5 files:\t" + str(len([name for name in listdir(DEST_DIR_BENIGN_H5) if isfile(join(DEST_DIR_BENIGN_H5, name))])))
print("pt files:\t" + str(len([name for name in listdir(DEST_DIR_BENIGN_PT) if isfile(join(DEST_DIR_BENIGN_PT, name))])))

print("\nNo. of Cancer files copied:")
print("h5 files:\t" + str(len([name for name in listdir(DEST_DIR_CANCER_H5) if isfile(join(DEST_DIR_CANCER_H5, name))])))
print("pt files:\t" + str(len([name for name in listdir(DEST_DIR_CANCER_PT) if isfile(join(DEST_DIR_CANCER_PT, name))])))

print("\nNo. of Hyperplasia files copied:")
print("h5 files:\t" + str(len([name for name in listdir(DEST_DIR_HYPERPLASIA_H5) if isfile(join(DEST_DIR_HYPERPLASIA_H5, name))])))
print("pt files:\t" + str(len([name for name in listdir(DEST_DIR_HYPERPLASIA_PT) if isfile(join(DEST_DIR_HYPERPLASIA_PT, name))])))
