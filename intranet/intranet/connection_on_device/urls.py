from django.urls import path

from connection_on_device.views import AddConnection, DelConnection, path_to, all_connection, on_device, index

urlpatterns = [
	path('', index, name='dev_list'),
    path('<int:id_dev>/del_connection', DelConnection.as_view(), name='del_connection'),
	path('<int:id_dev>/path', path_to, name='path_to_dev'),
	path('<int:id_dev>/add_connection', AddConnection.as_view(), name='add_connection'),
	path('<int:id_dev>/all_connection', all_connection, name='all_connection'),
	path('<int:id_dev>/', on_device, name='connections_on_dev'),
]