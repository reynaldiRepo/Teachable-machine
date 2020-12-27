from django.shortcuts import render
from teachapp.models import Machine
from teachapp.models import MachineClass
# Create your views here.
def mainapp(request):
    context = {
        'Title' : "Teaching Machine",
        'SubTitle' : "Define your class, add dataset, make machine learn your data"
    }
    return render (request, 'index.html', context)

