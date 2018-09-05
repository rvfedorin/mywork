from django.urls import path

from connection_on_device import views

urlpatterns = [
	path('', views.index, name='connections'),
	path('<int:id_dev>/path', views.path_to, name='path_to_dev'),
	path('<int:id_dev>/all_connection', views.all_connection, name='all_connection'),
	path('<int:id_dev>/', views.on_device, name='connections_on_dev'),
]