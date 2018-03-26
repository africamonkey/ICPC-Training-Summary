import math

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from markdownx.utils import markdownify

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import TeamForm

from summary.models import Status
from summary.views import int_to_strlist, templatelist

def login_view(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(request.POST.get('next', '/') or reverse('index_page:index'))
	if request.method != 'POST':
		form = AuthenticationForm(request)
	else:
		form = AuthenticationForm(request, data = request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect(request.POST.get('next', '/') or reverse('index_page:index'))
	context = {'form': form}
	return render(request, 'users/login.html', context)

@login_required
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
	return render(request, 'users/register.html', context)

def list_users(request, page_id = 1):
	per_page = 20
	cnt = User.objects.count()
	tot_page = math.ceil(cnt / per_page)
	if cnt == 0:
		tot_page = 1
	users = User.objects.order_by('id')[(page_id - 1) * per_page : page_id * per_page]
	user_list = []
	for user in users:
		try:
			profile = UserProfile.objects.get(user = user)
		except ObjectDoesNotExist:
			profile = UserProfile.objects.create(user = user)
		if profile.team_name.strip() == "":
			profile.team_name = "(Undefined)"
		if profile.team_member_1.strip() == "":
			profile.team_member_1 = "(Undefined)"
		if profile.team_member_2.strip() == "":
			profile.team_member_2 = "(Undefined)"
		if profile.team_member_3.strip() == "":
			profile.team_member_3 = "(Undefined)"
		my_profile = {
			'id': user.id,
			'username': user.username,
			'team_name': profile.team_name,
			'team_member_1': profile.team_member_1,
			'team_member_2': profile.team_member_2,
			'team_member_3': profile.team_member_3,
		}
		user_list.append(my_profile)
	context = {
		'page_id': page_id,
		'tot_page': tot_page,
		'user_list': user_list,
	}
	return render(request, 'users/list_users.html', context)

def show_user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	profile = get_object_or_404(UserProfile, user=user)
	if request.user is not None:
		user_id = request.user.id
	else:
		user_id = 0
	if user_id is None:
		user_id = 0
	summary = Status.objects.filter(owner=profile).order_by('-contest')
	summarylist = []
	max_problem = 0
	for i in summary:
		if i.contest.num_of_problem > max_problem:
			max_problem = i.contest.num_of_problem
	for i in summary:
		status = []
		ac_s = int_to_strlist(i.ac_status, 4, i.contest.num_of_problem)
		for j in ac_s:
			s = ''
			if j == '1':
				s = '√'
			elif j == '2':
				s = 'O'
			elif j == '3':
				s = 'X'
			status.append(s)
		while len(status) < max_problem:
			status.append('')
		if i.contest.contest_type == 'Onsite':
			onsite_tag = 1
		else:
			onsite_tag = 0
		summarylist.append(templatelist(head=i.contest.id, body=status, tail=i.contest.name, date=i.contest.date, onsite_tag=onsite_tag))
	problem = []
	for i in range(0, max_problem):
		problem.append(chr(ord('A') + i))
	# summarylist is a list of class consisting of three variable: head, body, tail
	# each item in summarylist stand for one summary of this contest
	# head is contest.id of the summary
	# body is a list of contributor string of each problem
	# tail is contest.name
	context = {
		'user_c': user,
		'user_id': user_id,
		'profile': profile,
		'summarylist': summarylist,
		'problem': problem,
		'team_description_markdown': markdownify(profile.team_description)
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
		except ObjectDoesNotExist:
			profile = UserProfile.objects.create(user = request.user)
		team_form = TeamForm(instance = profile)
	else:
		team_form = TeamForm(request.POST)
		if team_form.is_valid():
			try:
				profile = UserProfile.objects.get(user = request.user)
			except ObjectDoesNotExist:
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

@login_required
def histories(request, page_id = 1):
	per_page = 20
	try:
		profile = UserProfile.objects.get(user = request.user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('users:modify_profiles'))
	histories = profile.history.all()
	cnt = histories.count()
	tot_page = math.ceil(cnt / per_page)
	if cnt == 0:
		tot_page = 1
	histories = histories.order_by('-history_date')[(page_id - 1) * per_page : page_id * per_page]
	context = {
		'page_id': page_id,
		'tot_page': tot_page,
		'histories': histories,
	}
	return render(request, 'users/histories.html', context)

@login_required
def view_history(request, history_id):
	try:
		profile = UserProfile.objects.get(user = request.user)
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('users:modify_profiles'))
	histories = profile.history.all()
	history = histories.filter(history_id=history_id).values()
	if history.count() == 0:
		return HttpResponseRedirect(reverse('users:modify_profiles'))
	else:
		history = history[0]
	team_form = TeamForm(data = history)
	context = {
		'team_form': team_form,
	}
	return render(request, 'users/modify_profiles.html', context)
