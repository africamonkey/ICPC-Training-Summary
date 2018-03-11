from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Contest
from .forms import ContestForm

def index(request):
	contest = Contest.objects.order_by('id')
	context = {'contest': contest}
	return render(request, 'contests/index.html', context)

def add_contest(request):
	if request.method != 'POST':
		form = ContestForm()
	else:
		form = ContestForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('index_page:index'))
	
	context = {'form': form}
	return render(request, 'contests/add_contest.html', context)

def display_contest(request, contest_id):
	contest = get_object_or_404(Contest, pk=contest_id)
	context = {'contest': contest}
	return render(request, 'contests/display_contest.html', context)

def edit_contest(request, contest_id):
	contest = get_object_or_404(Contest, pk=contest_id)
	if request.method != 'POST':
		form = ContestForm(instance = contest)
	else:
		form = ContestForm(instance = contest, data = request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('contests:display_contest', args=[contest.id]))
	
	context = {'contest': contest, 'form': form}
	return render(request, 'contests/edit_contest.html', context)
