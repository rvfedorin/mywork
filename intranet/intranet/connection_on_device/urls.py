from django.urls import path
from django.contrib.auth.decorators import login_required

from connection_on_device import views
from models_device.views import DeviceView

urlpatterns = [
	path('', DeviceView.as_view(), name='dev_list'),
    path('<int:id_dev>/del_connection', login_required(views.DelConnection.as_view()), name='del_connection'),
    path('<int:id_dev>/edit_connection/<int:id_con>', login_required(views.EditConnection.as_view()), name='edit_connection'),
	path('<int:id_dev>/path', views.path_to, name='path_to_dev'),
	path('<int:id_dev>/add_connection', login_required(views.AddConnection.as_view()), name='add_connection'),
	path('<int:id_dev>/all_connection', views.all_connection, name='all_connection'),
	path('<int:id_dev>/', views.on_device, name='connections_on_dev'),
]