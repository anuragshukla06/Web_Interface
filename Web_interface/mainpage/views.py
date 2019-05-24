from django.shortcuts import render,redirect
from .forms import EntryForm, AlterParametersForm
from .models import PreSavedData, Entry, CurrentParameters
from django.http import HttpResponse
from django.core.files import File
import datetime, os, django
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib.figure import Figure
from django.utils import timezone
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

theEntryForm = None
OFFSET = 15
nowD = None
endD = None
diffD = None
emergency = False
prevEmergencyTemp = None
# Create your views here.
def home(request):
    entryForm = EntryForm()
    AllInactiveEntry = Entry.objects.filter(running = False)[:5] #use len instead of None
    try:
        runningEntry = Entry.objects.get(running = True)
    except Entry.DoesNotExist:
        runningEntry = None
        global emergency
        emergency = False


    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            global nowD, endD
            endD = form.cleaned_data["end_date"]
            thisFruit = form.cleaned_data["fruit"]
            nowD = timezone.now()
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

    global diffD
    nowD = timezone.now()
    if emergency:
        notKeepable = 3
        return render(request, 'home.html', {"form": entryForm, 'AllInactiveEntry': AllInactiveEntry,
                                             "runningEntry": runningEntry, "endD": endD, "diffD": diffD,
                                             "notKeepable": notKeepable})
    return render(request, 'home.html', {"form": entryForm, 'AllInactiveEntry': AllInactiveEntry,
                                         "runningEntry": runningEntry, "endD": endD, "diffD": diffD})

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
        #----------------------------------
        try:
            CurrentParameters.objects.all().delete()
        except:
            p = 1 #code has to be written

        preSaved = PreSavedData.objects.get(fruit = current.fruit)

        currentParameters = CurrentParameters(temperature=preSaved.temperature,
                                              fruit = preSaved.fruit,
                                              relative_humidity = preSaved.relative_humidity)
        currentParameters.save()
        #--------------------------------------
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
    stopRunningHelper(item_id)
    return redirect(home)

def stopRunningHelper(item_id):
    entry = Entry.objects.get(pk=item_id)
    entry.running = False
    f = open('C:/media/test' + str(entry.id) + '.csv', 'r')
    myFile = File(f)
    entry.dataRecord = myFile
    CurrentParameters.objects.all().delete()
    entry.save()

def saveAndReceive(request, temperature, humidity, light):

    try:
        current = Entry.objects.get(running = True)

        ##if the storage time expires
        nowD = timezone.now()
        if endD is not None and endD <= nowD:
            stopRunningHelper(current.id)
            return HttpResponse(" ".join(["-1", "-1", "-1"]))

        currentParameters = CurrentParameters.objects.all()[0]

        global emergency
        if abs(int(currentParameters.temperature)-int(temperature)) >= OFFSET:
            emergency = True
        else:
            emergency = False

        file_name = 'C:/media/test' + str(current.id) + '.csv'
        f = open(file_name, 'a+')
        if os.stat(file_name).st_size == 0:
            f.write('temperature'+',humidity' + ',light' + ',date' + '\n')
        f.write(temperature+ ',' + humidity+','+light +","+ str(datetime.datetime.now()) + '\n')

        return HttpResponse(" ".join([str(currentParameters.temperature),
                                     str(currentParameters.relative_humidity),
                                      str(currentParameters.light)]))
    except Entry.DoesNotExist:
        emergency = False
        return HttpResponse(" ".join(["-1", "-1", "-1"]))

def Monitor(request):
    try:
        current = Entry.objects.get(running=True)
    except Entry.DoesNotExist:
        return HttpResponse("The warehouse currently is not in operation")
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
def MonitorCollectiveImage(request, id):
    id = int(id)
    if id == -1:
        current = Entry.objects.get(running=True)
    else:
        current = Entry.objects.get(pk=id)
    file_name = 'C:/media/test' + str(current.id) + '.csv'
    data = pd.read_csv(file_name)
    data['date'] = pd.to_datetime(data['date'])

    fig = Figure()
    plt.subplot(3,1,1)
    plt.plot(data['date'], data['temperature'], label='temperature')
    plt.xlabel("Time")
    plt.ylabel("Temperature in °C")
    pylab.legend(loc='upper left')
    plt.subplot(3,1,2)
    plt.plot(data['date'], data['humidity'])
    plt.xlabel("Time")
    plt.ylabel("Relative Humidity")
    pylab.legend(loc='upper left')
    plt.subplot(3,1,3)
    plt.plot(data['date'], data['light'])
    plt.xlabel("Time")
    plt.ylabel("Light in Lux")
    pylab.legend(loc='upper left')

    FigureCanvas(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # return response
    return response

def history(request):
    items = Entry.objects.filter(running=False)
    return render(request, 'history.html', {'items': items})

def historyItemData(request, item_id):
    item = Entry.objects.get(pk=item_id)
    data = pd.read_csv(item.dataRecord)
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return HttpResponse(data_html)

def control(request):
    controlForm = AlterParametersForm()
    parameters = CurrentParameters.objects.all()
    currentParameters = -1
    if len(parameters) > 0:
        currentParameters = parameters[0]
    if request.method == "POST":
        form = AlterParametersForm(request.POST)
        if form.is_valid():
            temperature = form.cleaned_data["temperature"]
            relative_humidity = form.cleaned_data["relative_humidity"]
            light = form.cleaned_data["light"]
            currentParameters.relative_humidity = relative_humidity
            currentParameters.temperature = temperature
            currentParameters.light = light
            currentParameters.save()
            return redirect(control)
    else:
        if currentParameters == -1:
            return render(request, "control.html", {"form": controlForm, "current": currentParameters, "noParameters": 1})

        return render(request, "control.html", {"form": controlForm, "current": currentParameters, "noParameters": 0})


def about(request):
    return render(request, "index.html", {})

