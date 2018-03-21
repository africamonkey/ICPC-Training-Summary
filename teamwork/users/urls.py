from django.urls import path
from django.contrib.auth.views import login as auth_login

from . import views

app_name = 'users'

urlpatterns = [
	path('', views.list_users, name='list_users'),
	path('page/<int:page_id>/', views.list_users, name='list_users2'),
	path('login/', auth_login, {'template_name': 'users/login.html'}, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register, name='register'),
	path('profile/<int:user_id>/', views.show_user, name='show_user'),
	path('change_password/', views.change_password, name='change_password'),
	path('change_password_done/', views.change_password_done, name='change_password_done'),
	path('modify_profiles/', views.modify_profiles, name='modify_profiles'),
]
