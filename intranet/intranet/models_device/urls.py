from django.urls import path
from models_device import views

from models_device.views import DeviceView

urlpatterns = [
	path('', DeviceView.as_view(), name='device'),
	path('<str:region>/', DeviceView.as_view(), name='dev_list_region'),
	path('<str:region>/<str:city>/', DeviceView.as_view(), name='dev_list_city'),
]