from django.urls import path
from models_device import views

from models_device.views import DeviceView, DeviceCreate, DeviceUpdate

urlpatterns = [
	path('', DeviceView.as_view(), name='device'),
	path('add', DeviceCreate.as_view(), name='device_add'),
	path('edit/<int:dev_id>', DeviceUpdate.as_view(), name='device_edit'),
	path('<str:region>/', DeviceView.as_view(), name='dev_list_region'),
	path('<str:region>/<str:city>/', DeviceView.as_view(), name='dev_list_city'),
]