from django.urls import path
from django.contrib.auth.views import login

from . import views

app_name = 'users'

urlpatterns = [
	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/<int:user_id>/', views.show_user, name='show_user'),
]
