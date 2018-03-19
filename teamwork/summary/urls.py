from django.urls import path

from . import views

app_name = 'summary'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.home, name='home'),
    path('<int:user_id>/<int:contest_id>/', views.display_status, name='display_status'),
    path('<int:user_id>/<int:contest_id>/add_status/', views.add_status, name='add_status'),
    path('<int:user_id>/<int:contest_id>/edit_status/', views.edit_status, name='edit_status'),
]
