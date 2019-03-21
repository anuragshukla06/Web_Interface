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
import io, PIL, PIL.Image

def Monitor(request):
    current = Entry.objects.get(running=True)
    file_name = 'C:/media/test' + str(current.id) + '.csv'
    data = pd.read_csv(file_name)
    data['date'] = pd.to_datetime(data['date'])

    fig = Figure()
    plt.plot(data['date'], data['temperature'])

    FigureCanvas(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    #return response
    return response
    # Send buffer in a http response the the browser with the mime type image/png set
