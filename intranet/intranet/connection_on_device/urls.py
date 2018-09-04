from django.urls import path

from connection_on_device import views

urlpatterns = [
	path('', views.index, name='index')
]