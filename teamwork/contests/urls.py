from django.urls import path

from . import views

app_name = 'contests'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('add_contest/', views.add_contest, name = 'add_contest'),
]
