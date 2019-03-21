from django.shortcuts import render,redirect
from .forms import EntryForm
from .models import PreSavedData, Entry
from django.http import HttpResponse
from django.core.files import File
import datetime, os, django
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io, PIL, PIL.Image, time

theEntryForm = None
f = None
# Create your views here.
def home(request):
    entryForm = EntryForm()
    AllInactiveEntry = Entry.objects.filter(running = False)[:5] #use len instead of None
    try:
        runningEntry = Entry.objects.get(running = True)
    except Entry.DoesNotExist:
        runningEntry = None


    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            endD = form.cleaned_data["end_date"]
            thisFruit = form.cleaned_data["fruit"]
            nowD = datetime.datetime.now()
            diff = endD.date()-nowD.date()
            diff = diff.days
            preSavedData = PreSavedData.objects.get(fruit = thisFruit)
            if diff > preSavedData.numberOfDays:
                return render(request, 'home.html', {"notKeepable": 1, "form": entryForm,
                                                                     "expectedDays": preSavedData.numberOfDays,
                                                                     "diff": diff,
                                                                     "fruit": thisFruit,
                                                                     "runningEntry": runningEntry})
            elif runningEntry is not None :
                return render(request, 'home.html', {"notKeepable": 2,
                                                     "form": entryForm,
                                                     'AllInactiveEntry': AllInactiveEntry,
                                                     "runningEntry": runningEntry})
            else:
                global theEntryForm
                theEntryForm = form
                return redirect(afterValidateSuccess)



        else:
            HttpResponse("OOPS Something went wrong. Check your internet connection.")

    return render(request, 'home.html', {"form": entryForm, 'AllInactiveEntry': AllInactiveEntry,
                                         "runningEntry": runningEntry})

def afterValidateSuccess(request):
    global theEntryForm
    global f
    if request.method == "POST":
        theEntryForm.save()
        current = Entry.objects.latest('id')
        f = open('C:/media/test' + str(current.id) + '.csv', 'w')
        # myFile = File(f)
        # current.dataRecord = myFile
        current.running = True
        current.save()
        return redirect(home)

    if theEntryForm.is_valid():
        endD = theEntryForm.cleaned_data["end_date"]
        thisFruit = theEntryForm.cleaned_data["fruit"]
        startDate = datetime.datetime.now()
        nowD = datetime.datetime.now()
        diff = endD.date()-nowD.date()
        diff = diff.days
        preSaved = PreSavedData.objects.get(fruit = thisFruit)
        return render(request, 'afterValidateSuccess.html',
                      {"notKeepable": 0,
                       "form": theEntryForm,
                       "fruit": thisFruit,
                       "start": startDate,
                       "diff": diff,
                       "end": endD,
                       "preSaved": preSaved
                       })

def stopRunningConfirmation(request, item_id):
    return render(request, 'stopRunningConfirmation.html', {'item_id': item_id})

def stopRunning(request, item_id):
    entry = Entry.objects.get(pk=item_id)
    entry.running = False
    f = open('C:/media/test' + str(entry.id) + '.csv', 'r')
    myFile = File(f)
    entry.dataRecord = myFile
    entry.save()
    return redirect(home)

def saveAndReceive(request, temperature, humidity, light):
    current = Entry.objects.get(running = True)
    now = datetime.datetime.now()
    file_name = 'C:/media/test' + str(current.id) + '.csv'
    f = open(file_name, 'a+')
    if os.stat(file_name).st_size == 0:
        f.write('temperature'+',humidity' + ',light' + ',date' + '\n')
    f.write(temperature+ ',' + humidity+','+light +","+ str(now) + '\n')
    return HttpResponse(temperature + humidity+light)

def Monitor(request):
    return render(request, 'monitorBase.html')
    # current = Entry.objects.get(running=True)
    # file_name = 'C:/media/test' + str(current.id) + '.csv'
    # data = pd.read_csv(file_name)
    # data['date'] = pd.to_datetime(data['date'])
    #
    # fig = Figure()
    # plt.plot(data['date'], data['temperature'])
    #
    # FigureCanvas(fig)
    #
    # buf = io.BytesIO()
    # plt.savefig(buf, format='png')
    # plt.close(fig)
    # response = HttpResponse(buf.getvalue(), content_type='image/png')
    # #return response
    # return response
    # Send buffer in a http response the the browser with the mime type image/png set
def MonitorCollectiveImage(request):
    current = Entry.objects.get(running=True)
    file_name = 'C:/media/test' + str(current.id) + '.csv'
    data = pd.read_csv(file_name)
    data['date'] = pd.to_datetime(data['date'])

    fig = Figure()
    plt.subplot(3,1,1)
    plt.plot(data['date'], data['temperature'])
    plt.subplot(3,1,2)
    plt.plot(data['date'], data['humidity'])
    plt.subplot(3,1,3)
    plt.plot(data['date'], data['light'])

    FigureCanvas(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # return response
    return response
