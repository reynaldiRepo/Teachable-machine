from django.shortcuts import render
from teachapp.models import Machine
from teachapp.models import MachineClass
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import Http404

import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import urllib

from binascii import a2b_base64
import os
import shutil

# for keras modul / cnn modul
from cnn.CNN import CNN
from cnn.KerasCallback import TrainingCallback

#for write log training
import asyncio
from teachapp.consumer import doSendLogTraining

#for unique string web socket
import uuid 

from django.views.static import serve

# Views Apps / controller
def mainapp(request):
    context = {
        'Title' : "Teaching Machine",
        'SubTitle' : "Define your class, add dataset, make machine learn your data",
        'RoomCode' : uuid.uuid4().hex[:6].upper()
    }

    tomorrow = datetime.now() + timedelta(days = 1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

    response = render (request, 'index.html', context)
    response.set_cookie("RoomCode", "teachapp_"+context['RoomCode'], expires=expires)

    for m in Machine.objects.all():
        shutil.rmtree(m.Directory)
        print(m.id)
        m.delete()
    for mc in MachineClass.objects.all():
        print(mc.id)
        mc.delete()

    return response


def starttrain(request):    

    post = request.POST

    #validate request
    if post == None:
        return JsonResponse({"status":400, "msg":"Forbidden"}, safe=False)

    if request.COOKIES.get('RoomCode') == None:
        return JsonResponse({"status":400, "msg":"Forbidden"}, safe=False)

    

    data = json.loads(str(post.get('data')))
    newMachine = Machine();

    # get date time for machine name
    now = datetime.now(tz=timezone.utc)
    dt_string = now.strftime("%d%m%Y%H%M%S")
    #time for created time

    #get roodir
    rootdir = os.getcwd()
    
    #assign data machine
    newMachine.Name = "M-"+dt_string
    newMachine.Created = now
    newMachine.Directory = os.path.join(rootdir, "teachapp", "static", "UserData",newMachine.Name)
    newMachine.epoch = str(post.get('epoch'));
    newMachine.batch = str(post.get('batch'));
    newMachine.learningrate = str(post.get('learningrate'));

    os.makedirs(newMachine.Directory)

    newMachine.save();
    
    #write log file has readed
    asyncio.run(doSendLogTraining(RoomCode=request.COOKIES.get('RoomCode'), Log="Examine Your Dataset"));

    #iterate label on json data
    for i in data.keys():
        indexImage = 1;
        os.makedirs(os.path.join(newMachine.Directory,i))
        classdir = os.path.join(newMachine.Directory,i)
        newClass = MachineClass(Name=i, Machine_ID = str(newMachine.id))
        newClass.save();
        for urlraw in data[i] :
            imageurl = urllib.request.urlopen(urlraw)
            #write image to server
            with open(classdir+'/'+i+"-"+str(indexImage)+".png", 'wb') as f:
                f.write(imageurl.file.read());
            f.close();
            indexImage +=1;
    
    # //todo memeasukan ke model cnnn
    model = CNN(image_size_w = 80, image_size_h = 60, objectMachine = newMachine)
    print("Room Code", request.COOKIES.get('RoomCode'));
    # initiate Callback Keras
    callback = TrainingCallback(RoomName=request.COOKIES.get('RoomCode'))
    model.fittingModel(Callback=callback)

    return JsonResponse({"status":200, "msg":"success", "MachineID":newMachine.id}, safe=False)

def testing(request, machineid):
    
    if Machine.objects.filter(id=machineid).count() == 0:
        raise Http404;
    

    machine = Machine.objects.get(id=machineid)
    
    randomid = str("testing_")+uuid.uuid4().hex[:6].upper()+"_"+str(machineid)

    context = {
        'Title' : "Your machine are ready",
        'SubTitle' : "Start testing, Our Machine Has been learn your data",
        'Machine' : machine,
        'RoomCode' : randomid
    }

    response = render (request, 'testing.html', context)

    tomorrow = datetime.now() + timedelta(days = 1)
    tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie("RoomCode", "teachapp_"+context['RoomCode'], expires=expires)

    return response

def downloadModel(request, machineid):
    print(machineid)
    if Machine.objects.filter(id=machineid).count() == 0:
        raise Http404;
    machine = Machine.objects.get(id=machineid)
    file_path = machine.getExportFile();
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


