import math

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Contest
from .forms import ContestForm

from summary.models import Status
from summary.views import int_to_strlist, ctblist_to_strlist, templatelist

def index(request, page_id = 1):
	per_page = 20
	cnt = Contest.objects.count()
	tot_page = math.ceil(cnt / per_page)
	if cnt == 0:
		tot_page = 1
	contest = Contest.objects.order_by('-id')[(page_id - 1) * per_page : page_id * per_page]
	context = {
		'page_id': page_id,
		'tot_page': tot_page,
		'contest': contest,
	}
	return render(request, 'contests/index.html', context)

def add_contest(request):
	if request.method != 'POST':
		form = ContestForm()
	else:
		form = ContestForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('contests:index'))
	
	context = {'form': form}
	return render(request, 'contests/add_contest.html', context)

def display_contest(request, contest_id):
	contest = get_object_or_404(Contest, pk=contest_id)
	summary = Status.objects.filter(contest=contest)
	problem = []
	for i in range(0, contest.num_of_problem):
		problem.append(chr(ord('A') + i))
	summarylist = []
	for i in summary:
		status = []
		ac_s = int_to_strlist(i.ac_status, 4, contest.num_of_problem)
		ctb = ctblist_to_strlist(int_to_strlist(i.contributor, 8, contest.num_of_problem))
		for j in range(0, contest.num_of_problem):
			s = ''
			for k in ctb[j]:
				tmp = ''
				if int(k) == 1:
					tmp = i.owner.team_member_1
				elif int(k) == 2:
					tmp = i.owner.team_member_2
				elif int(k) == 4:
					tmp = i.owner.team_member_3
				s = s + tmp + ','
			if s == '':
				s = 'X'
			else:
				s = s[:-1]
			ck = None
			if ac_s[j] == '1':
				ck = True
			elif ac_s[j] == '2':
				ck = False
			status.append([ck, s])
		summarylist.append(templatelist(head=i.owner.user.id, body=status, tail=i.owner.team_name))

	# summarylist is a list of class consisting of three variable: head, body, tail
	# each item in summarylist stand for one summary of this contest
	# head is owner's userprofile.id of the summary
	# body is a list consisting ac status and contributor string of each problem
	# body[0] -> ac status, True=Solved, False=Upsolved, None=Unsolved
	# body[1] -> contributor string
	# tail is the owner's team_name
	context = {'contest': contest, 'summarylist': summarylist, 'problem': problem}
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
