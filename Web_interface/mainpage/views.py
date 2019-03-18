from django.shortcuts import render,redirect
from .forms import EntryForm
from .models import PreSavedData, Entry
from django.http import HttpResponse
import datetime

theEntryForm = None
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
    if request.method == "POST":
        theEntryForm.save()
        current = Entry.objects.latest('start_date')
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
    entry.save()
    return redirect(home)
