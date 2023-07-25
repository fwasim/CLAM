from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil

PATH_TO_EXCEL_FILE = '/Users/farhanahmedwasim/Desktop/MEng/Final project/dataset_images_100_percent.xlsx'
FEATURES_DIR = '/Users/farhanahmedwasim/Desktop/MEng/Final project/Image features'
FEATURES_DIR_H5 = FEATURES_DIR + '/h5_files'
FEATURES_DIR_PT = FEATURES_DIR + '/pt_files'
DEST_DIR = ''
DEST_DIR_BENIGN = DEST_DIR + '/Benign'
DEST_DIR_BENIGN_H5 = DEST_DIR_BENIGN + '/FEATURES_DIRECTORY_MATTHEW/h5_files'
DEST_DIR_BENIGN_PT = DEST_DIR_BENIGN + '/FEATURES_DIRECTORY_MATTHEW/pt_files'
DEST_DIR_CANCER = DEST_DIR + '/Cancer'
DEST_DIR_CANCER_H5 = DEST_DIR_CANCER + '/FEATURES_DIRECTORY_MATTHEW/h5_files'
DEST_DIR_CANCER_PT = DEST_DIR_CANCER + '/FEATURES_DIRECTORY_MATTHEW/pt_files'
DEST_DIR_HYPERPLASIA = DEST_DIR + '/Hyperplasia'
DEST_DIR_HYPERPLASIA_H5 = DEST_DIR_HYPERPLASIA + '/FEATURES_DIRECTORY_MATTHEW/h5_files'
DEST_DIR_HYPERPLASIA_PT = DEST_DIR_HYPERPLASIA + '/FEATURES_DIRECTORY_MATTHEW/pt_files'

onlyfiles = [f for f in listdir(FEATURES_DIR_H5) if isfile(join(FEATURES_DIR_H5, f))]

df = pd.read_excel(PATH_TO_EXCEL_FILE)
print('\nThis is how the excel file looks like:\n')
print(df.head())

print('\nHow many labels are there:\n')
print(df['Label'].value_counts())
ids = list(df['Participant ID'])

excluded_df = None

for i in onlyfiles:
    file_name = int(i.split('.')[0])
    df = df[df['Participant ID'] == file_name]

    if df.shape[0] == 1:
        label = df["Label"].to_string()

        if label == 'Benign':
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_BENIGN_H5)
            shutil.copyfile(FEATURES_DIR_PT + '/' + i, DEST_DIR_BENIGN_PT)
        elif label == 'Neoplasia':
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_CANCER_H5)
            shutil.copyfile(FEATURES_DIR_PT + '/' + i, DEST_DIR_CANCER_PT)
        else:
            shutil.copyfile(FEATURES_DIR_H5 + '/' + i, DEST_DIR_HYPERPLASIA_H5)
            shutil.copyfile(FEATURES_DIR_PT + '/' + i, DEST_DIR_HYPERPLASIA_PT)
    else:
        if excluded_df == None:
            excluded_df = df
        else:
            excluded_df.append(df)

print("\nNo. of Benign files copied:")
print("h5 files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_BENIGN_H5, name))]))
print("pt files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_BENIGN_PT, name))]))

print("\nNo. of Cancer files copied:")
print("h5 files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_CANCER_H5, name))]))
print("pt files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_CANCER_PT, name))]))

print("\nNo. of Hyperplasia files copied:")
print("h5 files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_HYPERPLASIA_H5, name))]))
print("pt files:\t" + len([name for name in listdir('.') if isfile(join(DEST_DIR_HYPERPLASIA_PT, name))]))