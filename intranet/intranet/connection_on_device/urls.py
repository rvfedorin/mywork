from django.urls import path

from connection_on_device import views

urlpatterns = [
	path('', views.index, name='connections'),
	path('<int:id_dev>/', views.on_device, name='connections_on_dev'),
]