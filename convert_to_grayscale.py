# -*- coding: utf-8 -*-
"""
Open Endometrial slides for inspection

Created on Tue Jul 20 14:01:11 2021

@author: Daniel
"""
# import slideio
import openslide
import matplotlib.pyplot as plt
import os
import sys
from PIL import Image
import datetime
from skimage.color import rgb2gray

WSI_size = 4096

def load_slideio(path, image_name, dest_path='./', WSI_size=(38000,43000)):
    #loads *.svs images and returns a list of images
    if image_name[-4:] != '.svs':
        return
    
    # path = os.path.join(root_path, img_name)
    # slide = slideio.open_slide(path, 'SVS')
    slide = openslide.open_slide( os.path.join(path, image_name))
    image = slide.read_region((0, 0), 0, WSI_size)
    # scene = slide.get_scene(0)
    # image = scene.read_block(size=WSI_size)
    
    # rgb_image = image.convert('RGB')

    # gray = rgb2gray(rgb_image)
    
    # gray_img = Image.fromarray(gray, mode="L")
    
    gray_img = image.convert('L')
    
    gray_img.save(os.path.join(dest_path, image_name.split('.')[0]+'.jpeg'))
    # print('Saved image '+path)
    return


#root_path = r'\\192.168.1.10\Data\HDD_Mt_Sinai\IMAGES'
root_path = sys.argv[1]

print(os.listdir(root_path))
dest_path = '/scratch/d/dsussman/fawasim/wsi_jpg_grey'+'_'+datetime.datetime.now().strftime('%Y_%h_%d__%H_%m')

if not os.path.exists(dest_path):
     os.mkdir(dest_path)

folders = ['Cancer', 'Atypical_hyperplasia', 'Hyperplasia_without_Atypia']

counter=0

for folder in folders:
    if not os.path.exists(os.path.join(dest_path, folder)):
        os.mkdir(os.path.join(dest_path, folder))
    if folder == 'Hyperplasia without Atypia':
        for year in os.listdir(os.path.join(root_path, folder)):
            if not os.path.exists(os.path.join(dest_path, folder, year)):
                os.mkdir(os.path.join(dest_path, folder, year))
            for img in os.listdir(os.path.join(root_path, folder, year)):
                if not os.path.exists(os.path.join(dest_path, folder, year, img.split('.')[0] + '.jpeg')):
                    print(img)
                    counter+=1
                    load_slideio(os.path.join(root_path, folder, year),img, os.path.join(dest_path, folder, year))
    else:
        for img in os.listdir(os.path.join(root_path, folder)):
            if not os.path.exists(os.path.join(dest_path, folder, img.split('.')[0] + '.jpeg')):
                print(img)
                counter+=1
                load_slideio(os.path.join(root_path, folder), img, os.path.join(dest_path, folder))