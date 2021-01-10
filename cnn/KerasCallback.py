from keras.callbacks import Callback
import asyncio
from teachapp.consumer import doSendLogTraining

class TrainingCallback (Callback):
    
    def __init__(self, RoomName):
        super(TrainingCallback, self).__init__()

        # to send callback message to user
        self.RoomName = RoomName;
    
    def on_train_begin(self, logs=None):
        keys = list(logs.keys())
        asyncio.run(doSendLogTraining(RoomCode=self.RoomName, Log="Start Training"))
        print ("Starting training")

    def on_train_end(self, logs=None):
        keys = list(logs.keys())
        asyncio.run(doSendLogTraining(RoomCode=self.RoomName, Log="Training Finished"))
        print("Training End")

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())
        asyncio.run(doSendLogTraining(RoomCode=self.RoomName, Log="Training Run On Epoch "+str(epoch)))
        print("Training Run On Epoch "+str(epoch))