# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import layers
import asyncio

from asgiref.sync import sync_to_async

#load models databse
from teachapp.models import Machine
from cnn.CNN import ModelLoader

#for write image
import urllib
import os
import uuid


class TestingConsumer(AsyncWebsocketConsumer):
    # function to get Database machine with sync to async
    @sync_to_async
    def getMachine(self, machineID):
        return Machine.objects.get(id=machineID)

    #function to get Cnn Model
    @sync_to_async
    def getCnnModel(self, MachineObject):
        return ModelLoader(objectMachine=MachineObject)

    #convert dataurl from user to image
    @sync_to_async
    def dotest(self, urlraw):
        model = self.loadedmodel.model
        imageurl = urllib.request.urlopen(urlraw)
        #write image to server
        dumpingdir = os.path.join(self.MachineObject.Directory, "testing_dump")
        if not os.path.isdir(dumpingdir):
            os.makedirs(dumpingdir)
        
        filepath = os.path.join(dumpingdir , uuid.uuid4().hex[:6].upper()+".png");
        with open( filepath , 'wb') as f:
            f.write(imageurl.file.read());
        f.close();

        prediction = self.loadedmodel.makepredict(filepath)

        return prediction

    async def connect(self):
        #make konstan on testing or training
        self.SocketType = "training"

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'teachapp_%s' % self.room_name
        
        # Join room group training or testing
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print("room_name connected : ",self.room_group_name)

        #make socket connection
        await self.accept()

        #for testing case
        self.loadedmodel = None
        self.MachineObject = None

        if "testing" in self.room_group_name :
            self.SocketType = "testing"
            
            # get machine object
            machineID = self.room_group_name.split("_")[-1]
            print("Machine ID = ", machineID)
            Machine = await self.getMachine(machineID)
            self.MachineObject = Machine

            #load cnn model
            Cnn = await self.getCnnModel(self.MachineObject)
            self.loadedmodel = Cnn

            # send message o user is machine ready
            await TestingConsumer.sendMachineReady(RoomCode=self.room_group_name, Log="Machine Ready")
            print("socket_testing_state")

        else :
            print("socket_training_state")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # check is massage from client for testing model
        if "state" in text_data_json :
            if text_data_json['state'] == "send_data_test":
                test = await self.dotest(urlraw = text_data_json['dataurl'])
                type_input = text_data_json['type_input']
                await TestingConsumer.sendTestingResult(RoomCode=self.room_group_name, data=test, type_input=type_input)
                print(test)

        else :
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'listen_msg',
                    'message': message
                }
            )

    # Receive message from room group
    async def listen_msg(self, event):
        message = event['message']
        print("msg from room ", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def machine_ready(self, event):
        message = event['message']
        print("msg from room ", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'state' : "machine_ready"
        }))

    # testing_result
    async def testing_result(self, event):
        message = event['message']
        data = event['data']
        type_input = event['type_input']
        print("msg from room ", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'state' : "testing_result",
            'data' : data,
            'type_input' : type_input
        }))

    async def sendLogTraining(RoomCode ,Log):
        channles = layers.get_channel_layer()
        await channles.group_send(
            RoomCode,
            {
                'type': 'listen_msg',
                'message': Log
            }
        )

    async def sendMachineReady(RoomCode ,Log):
        channles = layers.get_channel_layer()
        await channles.group_send(
            RoomCode,
            {
                'type': 'machine_ready',
                'message': Log
            }
        )

    async def sendTestingResult(RoomCode ,data, type_input):
        channles = layers.get_channel_layer()
        await channles.group_send(
            RoomCode,
            {
                'type': 'testing_result',
                'message': "Testing Result",
                'data' : data,
                'type_input' : type_input
            }
        )

    

        


async def doSendLogTraining(RoomCode ,Log):
    res = await asyncio.gather(TestingConsumer.sendLogTraining(RoomCode=RoomCode, Log=Log))
    return res
    
