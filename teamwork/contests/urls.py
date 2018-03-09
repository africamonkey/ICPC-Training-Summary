from django.urls import path

from . import views

app_name = 'contests'

urlpatterns = [
	path('', views.index, name = 'index')
]
