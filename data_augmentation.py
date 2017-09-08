"""
Author: Annus Zulfiqar
Program: data_augmentation.py 
Date: 07-09-17
Usage: Meant for doing some handy data augmentation on small object detection datasets 
Calling: Pass it the images, annotations and the destination folders  
"""

import os 
import cv2
import argparse
from log import log
log = log().log
import xml.etree.ElementTree as et
log('Imports successful!')

# translates the image by x, as well as the bounding_box in the direction passed as
# a keyword arguement
def translate(**kwargs):
    if len(kwargs) is not 4:
        raise ValueError('{} args passed. 4 needed'.format(len(locals())))
    directions = ['up', 'down', 'right', 'left']
    for key in kwargs:
        if key is 'image':
            image_array = kwargs[key]
        elif key is 'coords':
            coords = kwargs[key]
            x_min, y_min, x_max, y_max = map(int, coords)
        elif key is 'displacement':
            x = kwargs[key]
        elif key is 'direction':
            direction = kwargs[key]
            if direction not in directions:
                raise ValueError('Invalid value \'{}\' in direction.\n\
Possible Values: {}'.format(direction, directions))
        else: 
            raise KeyError('Invalid key \'{}\' keys'.format(key))
        

def rotate():
    log('total images: {}'.format(len(images)))
    for i, image_name in enumerate(images, 1):
        im = cv2.imread(os.path.join(path_to_folder, image_name), 1)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 800, 800)
        cv2.moveWindow('image', 0, 0)
        cv2.imshow('image', im)
        new_image = im.copy()
        saved = False
        read_key = cv2.waitKey(33)
        while not saved:
            while read_key == -1: read_key = cv2.waitKey(33)
            if read_key is 0xFF & ord('r'):
                new_image = imutils.rotate(new_image, -90)
                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('image', 800, 800)
                cv2.moveWindow('image', 0, 0)
                cv2.imshow('image', new_image)
                read_key = -1
                time.sleep(0.1)
            if read_key is 0xFF & ord('s'):
                cv2.imwrite(os.path.join(dest_folder, image_name), new_image)
                verbose = 'image#'+str(i+1)+' saved'
                log(verbose, cute=True)
                saved = True
                read_key = -1
                time.sleep(0.1)
    log()

def main():
    parser = argparse.ArgumentParser(description='this file augments obj_det dataset')
    parser.add_argument('--if', '--image_folder', type=str, dest='image_folder',
        help='image folder')
    parser.add_argument('--xf', '--xml_folder', type=str, dest='xml_folder',
        help='xml folder')
    parser.add_argument('--idf', '--image_dest_folder', type=str, dest='image_dest_folder',
        help='image destination folder')
    parser.add_argument('--xdf', '--xml_dest_folder', type=str, dest='xml_dest_folder',
        help='xml destination folder')
    args = parser.parse_args()

    images_folder = args.image_folder 
    xmls_folder = args.xml_folder
    images_dest = args.image_dest_folder
    xmls_dest = args.xml_dest_folder

    # create list of all xmls
    roots_list = [(xml.replace('.xml', ''), et.parse(os.path.join(xmls_folder, xml)).getroot())
        for xml in os.listdir(xmls_folder)]
    log('All xml roots acquired')
    for idx, (file_name, root) in enumerate(roots_list, 1):
        log('on image {} ({} of {})'.format(file_name, idx, len(roots_list)), cute=True)
        x_min = root.find('object').find('bndbox').find('xmin').text
        y_min = root.find('object').find('bndbox').find('ymin').text
        x_max = root.find('object').find('bndbox').find('xmax').text
        y_max = root.find('object').find('bndbox').find('ymax').text

        translate(image=cv2.imread(os.path.join(images_folder, file_name+'.jpg'), 1),
            coords=(x_min, y_min, x_max, y_max), displacement=10, direction='right')
    log()

if __name__ == '__main__':
    log('Entering main routine') 
    main()











