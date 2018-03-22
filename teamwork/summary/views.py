import math

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from markdownx.utils import markdownify

from contests.models import Contest
# from users.models import UserProfile
from .models import Status
from .forms import StatusForm


def strlist_to_int(strlist, rankpos):
    ans = 0
    w = 1
    for i in strlist:
        ans += w * int(i)
        w *= rankpos
    return ans


def int_to_strlist(ans, rankpos, rank):
    strlist = []
    for i in range(0, rank):
        strlist.append(str(ans % rankpos))
        ans //= rankpos
    return strlist


def ctblist_to_strlist(ctb):
    strlist = []
    for i in ctb:
        tmp = []
        w = int(i)
        if ((w & 1) == 1):
            tmp.append('1')
        if ((w & 2) == 2):
            tmp.append('2')
        if ((w & 4) == 4):
            tmp.append('4')
        strlist.append(tmp)
    return strlist


class templatelist():
    def __init__(self, head, body, tail, date, onsite_tag, *args, **kwargs):
        self.head = head
        self.body = body
        self.tail = tail
        self.date = date
        self.onsite_tag = onsite_tag


@login_required
def index(request):
    user = get_user(request)
    return HttpResponseRedirect(reverse('summary:home', args=[user.id]))


def home(request, user_id):
    contest = Contest.objects.order_by('id')
    context = {'contest': contest, 'user_id': user_id}
    return render(request, 'summary/index.html', context)


def display_status(request, user_id, contest_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_object_or_404(User, pk=user_id)
    try:
        summary = Status.objects.get(contest=cts, owner=user.userprofile)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('summary:add_status', args=[user_id, contest_id]))
    problem = []
    for i in range(0, cts.num_of_problem):
        problem.append(chr(ord('A') + i))
    status = []
    ac_s = int_to_strlist(summary.ac_status, 4, cts.num_of_problem)
    ctb = ctblist_to_strlist(int_to_strlist(summary.contributor, 8, cts.num_of_problem))
    for j in range(0, cts.num_of_problem):
        s = ''
        for k in ctb[j]:
            tmp = ''
            if int(k) == 1:
                tmp = summary.owner.team_member_1
            elif int(k) == 2:
                tmp = summary.owner.team_member_2
            elif int(k) == 4:
                tmp = summary.owner.team_member_3
            s = s + tmp + '<br />'
        if s == '':
            s = 'X'
        else:
            s = s[:-6]
        ck = None
        if ac_s[j] == '1':
            ck = True
        elif ac_s[j] == '2':
            ck = False
        status.append([ck, s])
    if cts.contest_type == 'Onsite':
        onsite_tag = 1
    else:
        onsite_tag = 0
    summarylist = templatelist(
        head=summary.owner.user.id,
        body=status,
        tail=summary.owner.team_name,
        date=cts.date,
        onsite_tag=onsite_tag,
    )
    context = {
        'status': summary,
        'summary_markdown': markdownify(summary.summary),
        'summary': summarylist,
        'problem': problem,
    }
    return render(request, 'summary/display_status.html', context)


@login_required
def edit_status(request, user_id, contest_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:index'))
    try:
        status = Status.objects.get(owner=user.userprofile, contest=cts)
        tag = 'Edit'
    except ObjectDoesNotExist:
        status = None
        tag = 'Add'
    if request.method != 'POST':
        if status is not None:
            ac_s = int_to_strlist(status.ac_status, 4, cts.num_of_problem)
            ctb = ctblist_to_strlist(int_to_strlist(status.contributor, 8, cts.num_of_problem))
            initial_value = {}
            initial_value['summary'] = status.summary
            for i in range(0, cts.num_of_problem):
                initial_value['p' + str(i)] = ac_s[i]
                initial_value['c' + str(i)] = ctb[i]
        else:
            initial_value = None
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=initial_value)
    else:
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=request.POST)
        if form.is_valid():
            # convert string from fields to ac_status and contributor
            ac_s = []
            ctb = []
            for i in range(0, cts.num_of_problem):
                ac_s.append('3')
                ctb.append([])
            for key, value in form.cleaned_data.items():
                if key[0] == 'p':
                    ac_s[int(key[1:])] = value
                elif key[0] == 'c':
                    ctb[int(key[1:])] = str(strlist_to_int(value, 1))
            # rewrite the status
            if status is None:
                status = form.save(commit=False)
                status.owner = user.userprofile
                status.contest = cts
            status.summary = form.cleaned_data['summary']
            status.ac_status = strlist_to_int(ac_s, 4)
            status.contributor = strlist_to_int(ctb, 8)
            status.save()
            return HttpResponseRedirect(reverse(
                'summary:display_status',
                args=[user_id, contest_id]
            ))
    context = {'user_handle': user, 'contest': cts, 'form': form, 'tag': tag}
    return render(request, 'summary/edit_status.html', context)


@login_required
def histories(request, user_id, contest_id, page_id=1):
    per_page = 20
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:index'))
    try:
        status = Status.objects.get(contest=cts, owner=user.userprofile)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('summary:add_status', args=[user_id, contest_id]))
    histories = status.history.all()
    cnt = histories.count()
    tot_page = math.ceil(cnt / per_page)
    if cnt == 0:
        tot_page = 1
    histories = histories.order_by('-history_date')[(page_id - 1) * per_page: page_id * per_page]
    context = {
        'status_owner_id': user_id,
        'contest_id': contest_id,
        'page_id': page_id,
        'tot_page': tot_page,
        'histories': histories,
    }
    return render(request, 'summary/histories.html', context)


@login_required
def view_history(request, user_id, contest_id, history_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:index'))
    try:
        status = Status.objects.get(contest=cts, owner=user.userprofile)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('summary:add_status', args=[user_id, contest_id]))
    histories = status.history.all()
    history = histories.filter(history_id=history_id).values()
    if history.count() == 0:
        return HttpResponseRedirect(reverse('summary:index'))
    else:
        history = history[0]
    ac_s = int_to_strlist(history['ac_status'], 4, cts.num_of_problem)
    ctb = ctblist_to_strlist(int_to_strlist(history['contributor'], 8, cts.num_of_problem))
    initial_value = {}
    initial_value['summary'] = history['summary']
    for i in range(0, cts.num_of_problem):
        initial_value['p' + str(i)] = ac_s[i]
        initial_value['c' + str(i)] = ctb[i]
    form = StatusForm(contest_id=contest_id, user_id=user_id, data=initial_value)
    context = {'user_handle': user, 'contest': cts, 'form': form}
    return render(request, 'summary/edit_status.html', context)
