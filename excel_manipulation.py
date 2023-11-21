import os
import pandas as pd

filter = True
local = True

# This script takes the big excel file containing all labels and sublabels and 
# splits it to create 3 other excel files each corresponding to one of the 3 
# labels with their corresponding sublabels
PATH_TO_EXCEL_FILE_MIST = '/scratch/d/dsussman/fawasim/dataset_images_100_percent.xlsx'
PATH_TO_FILTER_LIST_MIST = '/scratch/d/dsussman/fawasim/filtered_images_clean_v1.csv'
PATH_TO_EXCEL_FILE_LOCAL = '/Users/farhanahmedwasim/Desktop/MEng/Final project/dataset_images_100_percent.xlsx'
PATH_TO_FILTER_LIST_LOCAL = '/Users/farhanahmedwasim/Desktop/MEng/Final project/filtered_images_clean_v1.csv'
PATH_TO_EXCEL_FILE = PATH_TO_EXCEL_FILE_LOCAL if local else PATH_TO_EXCEL_FILE_MIST
PATH_TO_FILTER_LIST = PATH_TO_FILTER_LIST_LOCAL if local else PATH_TO_FILTER_LIST_MIST
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

    # Only take cancer ones for now. Cancer = Neoplasia
    print("\nFiltering out the labels with " + category_lower_case  + ". This is how the filtered excel file looks like:\n")
    df = df[df['Label'] == category]
    print(df.head())

    # Dropping random columns
    print("\n Dropping random columns created by excel\n")
    df=df.drop(df.columns[[2, 6, 7, 10, 11, 12]], axis=1)
    print(df.head())

    # Renaming columns
    df = df.rename(columns={'Unnamed: 0':'case_id', 'Participant ID': 'slide_id'})
    print("\nRenaming columns\n")
    print(df.head())

    print('\nHow many sub labels are there:\n')
    print(df['encoded Sublabel'].value_counts())

    if category == 'Hyperplasia':
        EXCEL_FILE_DEST_PATH = os.getcwd() + '/dataset_' + category_lower_case + '.csv' if local else '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'
    elif category == 'Neoplasia':
        EXCEL_FILE_DEST_PATH = os.getcwd() + '/dataset_' + category_lower_case + '.csv' if local else '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'
    else:
        EXCEL_FILE_DEST_PATH = os.getcwd() + '/dataset_' + category_lower_case + '.csv' if local else '/scratch/d/dsussman/fawasim/Output/' + category + '/dataset_' + category_lower_case + '.csv'

    if filter:
        # Filtering the excel based on filter file
        print('\n==========================================================')
        print('Filtering this master excel based on the filter file which was created after pre-processing the images and removing random artifacts.')
        df2 = pd.read_csv(PATH_TO_FILTER_LIST)
        print('\nThis is how the filter excel file looks like:\n')
        print(df2.head())

        filter_list_ids = df2[df2['Label'] == category]['case_id'].to_list()
        master_list_ids = df['case_id'].to_list()
        print('\nLength of filter list ids: ' + str(len(filter_list_ids)))
        print('Length of master list ids: ' + str(len(master_list_ids)))

        print("\nSize of master excel before:")
        print(df.shape)

        for i in range(len(master_list_ids)):
            if master_list_ids[i] in filter_list_ids:
                filter_list_ids.remove(master_list_ids[i])
            else:
                df = df.drop(df[df['case_id'] == master_list_ids[i]].index)

        print("\nSize of master excel after:")
        print(df.shape)

        if len(filter_list_ids) > 0:
            print("Filter file has more ids than master file!!")
            raise Exception
    df.to_csv(EXCEL_FILE_DEST_PATH)
    # print(df.head())