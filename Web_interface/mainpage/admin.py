from django.contrib import admin
from .models import PreSavedData, Entry
# Register your models here.
admin.site.register(PreSavedData)
admin.site.register(Entry)