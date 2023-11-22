from os import listdir
from os.path import isfile, join
import pandas as pd
import shutil

# This file takes all the feature vectors of all images, refers to the excel file containing the labels
# and copies those feature vector files over to their appropriate folder

PATH_TO_EXCEL_FILE = '/scratch/d/dsussman/fawasim/filtered_images_clean_v1.csv'
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
ALL_PATCHES_DIRECTORY = '/scratch/d/dsussman/fawasim/patches-removed-artfacts'

allfiles = listdir(ALL_PATCHES_DIRECTORY)
print("\nNo. of files in source directory:")
print(str(len(allfiles)))

print('\nCorrecting all filenames with double extension in source folder...\n')

# Correcting those filesnames that have double extension
for f in allfiles:
    if isfile(join(ALL_PATCHES_DIRECTORY, f)):
        if f.find('.svs') != -1:
            newFileName = f.split('.')[0] + '.' + f.split('.')[2]
            print("Corrected filename from " + f + " to " + newFileName)
            dest = ""
            try:
                dest = shutil.move(join(ALL_PATCHES_DIRECTORY, f), join(ALL_PATCHES_DIRECTORY, newFileName))
            except Exception as e:
                print("\nException faced while renaming file " + f)
                print(e)

for folder in listdir(DEST_DIR):
    print('\n***********************************************************')
    print('Copying all the files for the ' + str.lower(folder) + ' category')
    print('*************************************************************')

    PATH_TO_EXCEL_FILE = DEST_DIR + '/' + folder + '/dataset_' + str.lower(folder) + '.csv'

    df = pd.read_csv(PATH_TO_EXCEL_FILE)
    print('\nThis is how the excel file looks like:\n')
    print(df.head())

    print('\nTotal number of files to be copied:')
    print(df.shape[0])

    i = 0
    for fileName in df['slide_id'].to_list():
        if isfile(join(ALL_PATCHES_DIRECTORY, str(fileName) + '.h5')):
            i+=1
            try:
                shutil.copyfile(join(ALL_PATCHES_DIRECTORY, str(fileName) + '.h5'), DEST_DIR + '/' + folder + '/RESULTS_DIRECTORY/patches/' + str(fileName) + '.h5')
            except Exception as e:
                print("\nException faced while copying file from " + join(ALL_PATCHES_DIRECTORY, str(fileName) + '.h5') + " to " +  DEST_DIR + '/' + folder + '/RESULTS_DIRECTORY/patches/' + str(fileName) + '.h5')
                print(e)

    print('\nNo. of files copied: ' + str(i))

print("\nNo. of Benign files copied:")
print(len(listdir(DEST_DIR + '/Benign/RESULTS_DIRECTORY/patches/')))

print("\nNo. of Cancer files copied:")
print(len(listdir(DEST_DIR + '/Neoplasia/RESULTS_DIRECTORY/patches/')))

print("\nNo. of Hyperplasia files copied:")
print(len(listdir(DEST_DIR + '/Hyperplasia/RESULTS_DIRECTORY/patches/')))
