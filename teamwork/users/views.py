from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
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
			profile = team_form.save(commit=False)
			profile.user = user
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

@login_required
def change_password(request):
	if request.method != 'POST':
		form = PasswordChangeForm(user = request.user)
	else:
		form = PasswordChangeForm(user = request.user, data = request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return HttpResponseRedirect(reverse('users:change_password_done'))
	context = {
		'form': form,
	}
	return render(request, 'users/change_password.html', context)

def change_password_done(request):
	return render(request, 'users/change_password_done.html')

@login_required
def modify_profiles(request):
	if request.method != 'POST':
		try:
			profile = UserProfile.objects.get(user = request.user)
		except:
			profile = UserProfile.objects.create(user = request.user)
		team_form = TeamForm(instance = profile)
	else:
		team_form = TeamForm(request.POST)
		if team_form.is_valid():
			try:
				profile = UserProfile.objects.get(user = request.user)
			except:
				profile = UserProfile.objects.create(user = request.user)
			profile.team_name = team_form.cleaned_data["team_name"]
			profile.team_member_1 = team_form.cleaned_data["team_member_1"]
			profile.team_member_2 = team_form.cleaned_data["team_member_2"]
			profile.team_member_3 = team_form.cleaned_data["team_member_3"]
			profile.team_description = team_form.cleaned_data["team_description"]
			profile.save()
			return HttpResponseRedirect(reverse('users:show_user', args=[request.user.id]))
	context = {
		'team_form': team_form,
	}
	return render(request, 'users/modify_profiles.html', context) 
