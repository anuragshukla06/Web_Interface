from django.contrib import admin
from .models import PreSavedData, Entry, CurrentParameters
# Register your models here.
admin.site.register(PreSavedData)
admin.site.register(Entry)
admin.site.register(CurrentParameters)