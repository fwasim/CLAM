import os
import pandas as pd

# This script takes the big excel file containing all labels and sublabels and 
# splits it to create 3 other excel files each corresponding to one of the 3 
# labels with their corresponding sublabels

PATH_TO_EXCEL_FILE = '/scratch/d/dsussman/fawasim/dataset_images_100_percent.xlsx'
# IMAGE_DIR = '/Users/farhanahmedwasim/Desktop/MEng/Final project/Raw WSIs/BENIGN'
categories = ['Benign', 'Neoplasia', 'Hyperplasia']

df = pd.read_excel(PATH_TO_EXCEL_FILE)
print('\nThis is how the excel file looks like:\n')
print(df.head())
print('\nHow many labels are there:\n')
print(df['Label'].value_counts())

for category in categories:
    df = pd.read_excel(PATH_TO_EXCEL_FILE)
    print('\n***********************************************************')
    print('Creating excel file for ' + category + ' images and sublabels')
    print('*************************************************************')
    category_lower_case = category[0].lower() + category[1:]

    # # Only take cancer ones for now. Cancer = Neoplasia
    print("\nFiltering out the labels with " + category_lower_case  + ". This is how the filtered excel file looks like:\n")
    df = df[df['Label'] == category]
    print(df.head())

    # # Dropping random columns
    print("\n Dropping random columns created by excel\n")
    df=df.drop(df.columns[[2, 6, 7, 10, 11, 12]], axis=1)
    print(df.head())

    # # Renaming columns
    df = df.rename(columns={'Unnamed: 0':'case_id', 'Participant ID': 'slide_id'})
    print("\nRenaming columns\n")
    print(df.head())

    print('\nHow many sub labels are there:\n')
    print(df['encoded Sublabel'].value_counts())

    if category == 'Hyperplasia':
        EXCEL_FILE_DEST_PATH = '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'
    elif category == 'Neoplasia':
        EXCEL_FILE_DEST_PATH = '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'
    else:
        EXCEL_FILE_DEST_PATH = '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'

    # Keep only the columns interested
#    print('\nKeeping only the columns needed. This is how the filtered excel file looks like::\n')
 #   df = df[['Participant ID', 'Label', 'Sublabel', 'encoded_label', 'encoded Sublabel']]
    df.to_csv(EXCEL_FILE_DEST_PATH)
    print(df.head())

# Reading the data from folder and filtering out rows that don't correspond to valid file names
# print('\n==========================================================')
# print('Reading the data from folder and filtering out rows that don\'t correspond to valid file names')
# def removeFileExtension(filename):
#     splitList = filename.split('.')
#     if splitList[-2] == 'svs':
#         splitList = splitList[0:-1]

#     if len(splitList) > 2:
#         return splitList[0] + '.' + splitList[1]
#     else:
#         return splitList[0]

# image_list = os.listdir(IMAGE_DIR)
# image_list = list(map(lambda filename : removeFileExtension(filename), image_list))
# print('\nNumber of images in \''+ IMAGE_DIR + '\': ' + str(len(image_list)))
# # print(image_list)

# excel_list = df['slide_id'].to_list()
# for id in excel_list:
#     # print('Id in excel list: ' + str(id))
#     # print('Id type: ', type(id))
#     if str(id) not in image_list:
#         # print('Id not found in image list: ' + str(id))
#         # print('Id type: ', type(id))
#         df = df[df.slide_id != id]

# print('\nHow many sub labels are there:\n')
# print(df['encoded Sublabel'].value_counts())

# df.loc[df['column_name'] == some_value]
# participant_id = df['Participant ID'].to_list()
# participant_id.sort()
# # print('Are the participant_id consecutive: ' + str(check_if_consecutive(participant_id)))
# dupes = find_duplicates(participant_id)
# print(dupes)
