from django.shortcuts import render
from teachapp.models import Machine
from teachapp.models import MachineClass
from django.http import JsonResponse
import json
from datetime import datetime
from datetime import timezone
import urllib

from binascii import a2b_base64
import os
import shutil

from cnn.CNN import CNN

# Views Apps / controller
def mainapp(request):
    context = {
        'Title' : "Teaching Machine",
        'SubTitle' : "Define your class, add dataset, make machine learn your data"
    }

    # cleaning database
    # for m in Machine.objects.all():
    #     shutil.rmtree(m.Directory)
    #     print(m.id)
    #     m.delete()
    # for mc in MachineClass.objects.all():
    #     print(mc.id)
    #     mc.delete() 

    # try get data
    machine = Machine.objects.get(id = 15)
    model = CNN(image_size_w = 80, image_size_h = 60, objectMachine = machine)
    model.fittingModel()
    

    return render (request, 'index.html', context)

def pagetry(request):
    return render (request, 'blank.html', {"data":"hallo"})


def starttrain(request):
    post = request.POST
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


    return JsonResponse({"status":200, "msg":"success"}, safe=False)