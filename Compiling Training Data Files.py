# Author: Joel Ahn
# Purpose: Because np.vstack function is computationally expensive and slows down the framerate, multiple training data files were created,
#          capturing different sections of the pre-made track. This file will compile all the training data files and collect them into a
#          single one. 

import numpy as np
import glob

print 'Loading Training Data'

training_data = glob.glob('Training_data_*.npz') #creates a tuple of file names
brake = np.array((0,0,0,0,1))
image_array = np.zeros((1,320*240))
label_array = np.zeros((1,5),int)
no_of_frames = 0
file_no = 1

for data_file in training_data: #Call each individual file in the training_data tuple

    print ('File no: %d' file_no)
    
    with np.load(data_file) as temp:
        train_temp = temp['training_data']
        labels_temp = temp['training_data_labels']
        no_of_frames += train_temp.shape[0]
        print train_temp.shape[0]

    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, labels_temp))

    file_no += 1

print ('Training Data Succesfully Loaded and Processed')
image_array = image_array[1:,:] #Array without the buffer zeros
label_array = label_array[1:,:] #Array without the buffer zeros
np.savez('The_training_data', training_data = image_array, training_data_labels = label_array) 
print no_of_frames
print image_array.shape
print label_array.shape


