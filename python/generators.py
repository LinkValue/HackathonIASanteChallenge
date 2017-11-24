import os
import numpy as np
import random
import scipy
import sys
import json
import PIL, PIL.Image
from PIL import Image as pil_image
import imageio

from scipy.ndimage import imread

def generate_arrays_from_bottleneck_folder(path, batch_size=32, target_size=(224,224)):
    '''
    Generator that reads the precomputed weights from the files
    and gives it to the trainer.
    
    It shuffles the entries on every epoch.
    '''
    labels = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    labels.sort()
    
    labels_map = {}
    for i, label in enumerate(labels):
        labels_map[label] = i
    all_images = []
    
    for i, label in enumerate(labels):
        images = [str(a) for a in os.listdir(os.path.join(path, label))]
        for image in images:
            all_images.append((label, image))
    while 1:
        
        random.shuffle(all_images)
        X = np.zeros((batch_size, target_size[0], target_size[1], 3))
        Y = np.zeros((batch_size, 1, len(labels)))
        for i in range(batch_size):
            entry = all_images[i]
            label = entry[0]
            image = entry[1]
            
            x = imread(os.path.join(path, label, image))
            # print(x.size)
            # if x.size != (target_size[0], target_size[1],3):
            #     resample = pil_image.NEAREST
            #     x = x.resize((target_size[0], target_size[1],3), resample)
            x = scipy.misc.imresize(x, target_size)

            x = x.astype('float32') / 255.
            X[i] = x
#            X[i] = x[:target_size[0], :target_size[1], 3]
            y = np.zeros((1, len(labels)))
            y[0, labels_map[label]] = 1
            Y[i] = y

        yield (X, Y)

# gen = generate_arrays_from_bottleneck_folder('/sharedfiles/challenge_data/data/train', batch_size=32, target_size=(224,224))

# for x, y in gen:
#     print(x.shape)
#     print(y.shape)

