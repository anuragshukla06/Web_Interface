from django import forms
import datetime
from .models import Entry

class EntryForm(forms.ModelForm):
    fruit = forms.CharField(max_length=200, label="Fruit")
    end_date = forms.DateTimeField(initial=datetime.datetime.today, label='Storage_Till');

    class Meta:
        model = Entry
        fields = ['fruit', 'end_date']