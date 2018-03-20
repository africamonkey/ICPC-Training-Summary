from django.urls import path

from . import views

app_name = 'contests'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('page/<int:page_id>/', views.index, name = 'index2'),
	path('add_contest/', views.add_contest, name = 'add_contest'),
	path('<int:contest_id>/', views.display_contest, name = 'display_contest'),
	path('<int:contest_id>/edit/', views.edit_contest, name = 'edit_contest'),
]
