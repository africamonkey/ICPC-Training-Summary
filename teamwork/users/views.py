from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import TeamForm

def login_view(request):
	if request.method != 'POST':
		form = AuthenticationForm(request)
	else:
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect(reverse('index_page:index'))
	context = {'form': form}
	return render(request, 'users/login.html', context)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('index_page:index'))

def register(request):
	if request.method != 'POST':
		user_form = UserCreationForm()
		team_form = TeamForm()
	else:
		user_form = UserCreationForm(request.POST)
		team_form = TeamForm(request.POST)
		if user_form.is_valid() and team_form.is_valid():
			user = user_form.save()
			profile = UserProfile.objects.create(user = user)
			profile.team_name = team_form.cleaned_data["team_name"]
			profile.team_member_1 = team_form.cleaned_data["team_member_1"]
			profile.team_member_2 = team_form.cleaned_data["team_member_2"]
			profile.team_member_3 = team_form.cleaned_data["team_member_3"]
			profile.team_description = team_form.cleaned_data["team_description"]
			profile.save()
			return HttpResponseRedirect(reverse('users:login'))
	context = {
		'user_form': user_form,
		'team_form': team_form,
	}
	print(team_form)
	return render(request, 'users/register.html', context)

def show_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	profile = get_object_or_404(UserProfile, user=user)
	context = {
		'user': user,
		'profile': profile,
	}
	return render(request, 'users/show_user.html', context)
