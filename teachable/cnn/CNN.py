
from keras.layers import Dense, Input, Dropout, Flatten, Conv2D,  Activation, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.models import load_model


import cv2
import os
import numpy as np



class CNN :
    
    def __init__(self, image_size_w, image_size_h, objectMachine):

        self.objectMachine = objectMachine

        self.nb_classes = objectMachine.getMachineClass().count()
        self.epoch = int(objectMachine.epoch)
        self.learning_rate = float(objectMachine.learningrate)
        self.batch = int(objectMachine.batch)
        self.path = objectMachine.Directory
        self.labelClass = objectMachine.getArrayLabelClass()
        self.image_size_w = image_size_w
        self.image_size_h = image_size_h

        # Initialising the CNN
        self.model = Sequential()

        # 1 - Convolution
        self.model.add(Conv2D(32,3,padding="same", activation="relu", input_shape=(self.image_size_h,self.image_size_w,3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Dense(self.nb_classes, activation="softmax"))

        opt = Adam(lr= self.learning_rate)
        self.model.compile(optimizer = opt , loss = 'categorical_crossentropy' , metrics = ['accuracy'])

        # initiate history variable for fitting data
        self.history = None
        self.x_train = []
        self.y_train = []

        #doing read Data
        self.readTrainData()
        
        self.getSummary()

    def readTrainData(self):
        #for test
        label = self.labelClass
        path = self.path

        #real code
        data = []
        for l in label :
            pathImage = os.path.join(path, l)
            num_label_class = label.index(l)
            print(pathImage)
            for img in os.listdir(pathImage):
                try:
                    img_arr = cv2.imread(os.path.join(pathImage, img))
                    resized_arr = cv2.resize(img_arr, (self.image_size_w, self.image_size_h))
                    data.append([ resized_arr , num_label_class])
                except Exception as e:
                    print(e)
        train = np.array(data)
        self.transformData(train)

    def transformData(self, train):
        
        # transofrm array training image data to array feature and target
        for feature, label in train:
            self.x_train.append(feature)
            self.y_train.append(label)
        
        # Normalize the data
        self.x_train = np.array(self.x_train) / 255
        self.x_train.reshape(-1, self.image_size_w, self.image_size_h, 1)
        
        # convert to ndarray
        self.y_train = np.array(self.y_train)

        # make categorical
        self.y_train = to_categorical(self.y_train, self.nb_classes)

        # asume that label is sorted same with self.labelClass
        print(self.labelClass)
        for label in self.labelClass:
            machineclass = self.objectMachine.getMachineClass().get(Name = label)
            if (machineclass):
                machineclass.ClassEncoding = self.labelClass.index(label)
                machineclass.save()


    def fittingModel(self, Callback):
        self.history = self.model.fit(self.x_train, self.y_train, 
        batch_size=self.batch,
        epochs=self.epoch,
        callbacks=[Callback])
        self.evaluate = self.model.evaluate(self.x_train, self.y_train, verbose=0)
        self.savingmodel()

    def savingmodel(self):
        path = self.path
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(os.path.join(path, "model.json"), "w") as json_file:
            json_file.write(model_json)
        json_file.close();
        # serialize model to HDF5
        self.model.save( os.path.join(path, "model.h5") )
        print("Saved model to disk")

    def getSummary(self):
        self.model.summary()


class ModelLoader():
    def __init__(self, objectMachine):
        self.objectMachine = objectMachine
        self.modelh5 = os.path.join(objectMachine.Directory, "model.h5")
        self.model = load_model(filepath=self.modelh5)
        self.model.summary()
    
    def makepredict(self, pathimage):
        img_arr = cv2.imread(pathimage)
        resized_arr = cv2.resize(img_arr, (80, 60))
        resized_arr = np.array([resized_arr])
        #normalize 
        dataTest = np.array(resized_arr) / 255
        # shape = (60, 80, 3)
        dataTest.reshape(-1, 80, 60, 1)
        # print(dataTest)

        prediction = self.model.predict(dataTest)
        print(prediction)
        label = self.objectMachine.getArrayLabelClass()
        result = {}
        for i in range (len(prediction[0])):
            result[label[i]] = float(prediction[0][i])
        return result

    


# # # testing
# newM = CNN( nb_classes= 2, epoch = 50, batch= 16 , learning_rate = 0.001, image_size_w= 80, image_size_h= 80)
# print(newM.x_train)
# print(newM.x_train[0].shape)
# print(newM.y_train)
# print(newM.y_train.shape)
# newM.fittingModel()

