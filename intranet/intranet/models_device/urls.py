from django.urls import path
from models_device import views

urlpatterns = [
	path('', views.index, name='device')
]