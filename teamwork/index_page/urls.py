from django.urls import path

from . import views

app_name = 'index_page'

urlpatterns = [
	path('', views.index, name = 'index')
]
