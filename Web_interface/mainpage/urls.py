from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('success/', views.afterValidateSuccess, name = "afterValidateSuccessUrl"),
    path('stopConfirmation/<int:item_id>', views.stopRunningConfirmation, name = "stopRunningConfirmationUrl"),
    path('stop/<int:item_id>', views.stopRunning, name = "stopRunningUrl")
]
