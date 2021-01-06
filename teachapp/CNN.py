
from keras.layers import Dense, Input, Dropout, GlobalAveragePooling2D, Flatten, Conv2D, BatchNormalization, Activation, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.datasets import mnist

# from teachapp.models import Machine
# from teachapp.models import MachineClass

import cv2
import os
import numpy as np


class CNN :
    
    def __init__(self, nb_classes, epoch, learning_rate):
        #create model
        # number of possible label values
        self.nb_classes = nb_classes

        # Initialising the CNN
        self.model = Sequential()

        # 1 - Convolution
        self.model.add(Conv2D(64,(3,3), padding='same', input_shape=(48, 48,1)))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        # 2nd Convolution layer
        self.model.add(Conv2D(128,(5,5), padding='same'))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        # 3rd Convolution layer
        self.model.add(Conv2D(512,(3,3), padding='same'))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        # 4th Convolution layer
        self.model.add(Conv2D(512,(3,3), padding='same'))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        # Flattening
        self.model.add(Flatten())

        # Fully connected layer 1st layer
        self.model.add(Dense(256))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.25))

        # Fully connected layer 2nd layer
        self.model.add(Dense(512))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.25))

        self.model.add(Dense(nb_classes, activation='softmax'))

        opt = Adam(lr = learning_rate)
        self.model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    def readTrainData(self):
        #for test
        label = ['Class-1', 'Class-2']
        path = "D:\django_project\teachable/teachapp/static/UserData/M-06012021053644";
        for l in label :
            pathImage = os.path.join(path, l)
            print(pathImage)

    def getSummary(self):
        return self.model.summary()


# testing
newM = CNN(2, 50, 0.001)
print(newM.getSummary());
newM.readTrainData()