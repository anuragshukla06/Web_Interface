from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('success/', views.afterValidateSuccess, name = "afterValidateSuccessUrl"),
    path('stopConfirmation/<int:item_id>', views.stopRunningConfirmation, name = "stopRunningConfirmationUrl"),
    path('stop/<int:item_id>', views.stopRunning, name = "stopRunningUrl"),
    path('saveAndReceive/<temperature>/<humidity>/<light>', views.saveAndReceive, name = "saveAndReceiveUrl"),
    path('Monitor/', views.Monitor, name="MonitorUrl"),
    path('monitorCollectiveImage/', views.MonitorCollectiveImage, name="MonitorCollectiveImageUrl"),
    # path('monitorHumidityImage/', views.MonitorHumidityImage, name="MonitorHumidityImageUrl"),
    # path('monitorLightImage/', views.MonitorLightImage, name="MonitorLightImageUrl"),
    # path('monitorTemperatureImage/', views.MonitorTemperatureImage, name="MonitorTemperatureImageUrl")

]
