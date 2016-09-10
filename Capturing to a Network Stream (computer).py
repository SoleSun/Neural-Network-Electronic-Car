#Author: Joel Ahn
#Purpose: Converts the computer into TCP and enables data collection from Raspberry Pi via IP and steering of Bluetooth car via Bluetooth Serial
import io
import socket
import struct
import serial
import msvcrt
import numpy as np
from PIL import Image
import time

#Initialize steps needed for RPI connection via IP
print('Setting up IP server')
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')

#Initialize steps needed for Arduino
print('Connecting with the Arduino')
arduino = serial.Serial('COM10', 9600) #Connects with the Arduino via bluetooth to relay commands
print('Connection succesfully established')

#Lists of variables
frame = 1 #numbers the saved image files sequentially
labels = np.zeros((5,5),int)
for i in range(5):
    labels[i,i] = 1 #indices 0-4 represent forward, left, right, back, and brake respectively
cmd_index = 5 #Variable that stores the current command and provides the labelling


#List of arrays 
image_array = np.zeros((1,320*240)) #initialize image data size
label_array = np.zeros((1,5), int) #initialize command data size


try:
  
    while True:
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        image_stream = io.BytesIO() #creates a temporary stream where images can be stored
        image_stream.write(connection.read(image_len))
        image_stream.seek(0)

        image = Image.open(image_stream).convert("L") # Opens the image and converts it to greyscale
        #image.save('Frame_%d.jpg' %frame, "JPEG") Removed in order to reduce computing requirement and increase framerate
        temp_data = np.asarray(image.getdata()).reshape(1,320*240) #Reduce image to pixel data


        if msvcrt.kbhit():
            keypress = msvcrt.getch()
            if keypress == '8':
                arduino.write('8')
                print('Going Forward')
                cmd_index = 0

            elif keypress == '4':
                arduino.write('4')
                print('Turning Left')
                cmd_index = 1

            elif keypress == '6':
                arduino.write('6')
                print('Turning right')
                cmd_index = 2

            elif keypress == '2':
                arduino.write('2')
                print('Reversing')
                cmd_index = 3

            elif keypress == '5':
                arduino.write('5')
                print('Braking')
                cmd_index = 4

            elif keypress == 'x':
                break

        if cmd_index != 5:
            image_array = np.vstack((image_array, temp_data)) #compile the image data
            label_array = np.vstack((label_array, labels[cmd_index])) #compile command data
            frame += 1


    #Make sure Arduino is braked before stopping TCP
    arduino.write('5')
    
    #Remove the filler first row of zeros
    training_data = image_array[1:, :]
    training_data_labels = label_array[1:, :]
    print (training_data.shape)
    print(training_data_labels.shape)

    #Save the file to an npz file
    np.savez('Training_data_', training_data = training_data, training_data_labels = training_data_labels)
    print('%d frames saved and ready for training' %(frame - 1))

    
    
finally:
    input('Press enter to continue')
    connection.close()
    server_socket.close()
