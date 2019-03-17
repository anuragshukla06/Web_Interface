from django.shortcuts import render,redirect
from .forms import EntryForm
from .models import PreSavedData
from django.http import HttpResponse
import datetime

theEntryForm = None
# Create your views here.
def home(request):
    entryForm = EntryForm()
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
                                                                     "fruit": thisFruit})
            else:
                global theEntryForm
                theEntryForm = form
                return redirect(afterValidateSuccess)



        else:
            vghcfyxtdezrx

    return render(request, 'home.html', {"form": entryForm})

def afterValidateSuccess(request):
    global theEntryForm
    if request.method == "POST":
        theEntryForm.save()
        return HttpResponse("SUCCESS")

    if theEntryForm.is_valid():
        endD = theEntryForm.cleaned_data["end_date"]
        thisFruit = theEntryForm.cleaned_data["fruit"]
        startDate = datetime.datetime.now()
        nowD = datetime.datetime.now()
        diff = endD.date()-nowD.date()
        diff = diff.days
        return render(request, 'afterValidateSuccess.html',
                      {"notKeepable": 0,
                       "form": theEntryForm,
                       "fruit": thisFruit,
                       "start": startDate,
                       "diff": diff,
                       "end": endD
                       })
