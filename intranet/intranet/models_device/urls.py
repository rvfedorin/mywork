from django.urls import path
from models_device import views

from models_device import views

urlpatterns = [
	path('', views.index, name='device'),
	path('<str:region>/', views.region, name='dev_list_region'),
	path('<str:region>/<str:city>', views.city, name='dev_list_city'),
]