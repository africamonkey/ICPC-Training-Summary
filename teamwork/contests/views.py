from django.shortcuts import render
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
