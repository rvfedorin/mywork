from django.urls import path
from django.contrib.auth.decorators import login_required

from models_device import views
from models_device.views import DeviceView, DeviceCreate, DeviceUpdate, DeviceDelete

urlpatterns = [
	path('', DeviceView.as_view(), name='device'),
	path('add', login_required(DeviceCreate.as_view()), name='device_add'),
	path('<str:region>/add', login_required(DeviceCreate.as_view()), name='device_add_reg'),
	path('<str:region>/<str:city>/add', login_required(DeviceCreate.as_view()), name='device_add_city'),
	path('delete', login_required(DeviceDelete.as_view()), name='device_delete'),
	path('edit/<int:dev_id>', login_required(DeviceUpdate.as_view()), name='device_edit'),
	path('<str:region>/', DeviceView.as_view(), name='dev_list_region'),
	path('<str:region>/<str:city>/', DeviceView.as_view(), name='dev_list_city'),
]