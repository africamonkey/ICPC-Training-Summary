from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user

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
    def __init__(self, head, body, tail, *args, **kwargs):
        self.head = head
        self.body = body
        self.tail = tail


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
        status = Status.objects.get(contest=cts, owner=user.userprofile)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('summary:add_status', args=[user_id, contest_id]))
    context = {'status': status, 'contest_id': contest_id, 'user_id': user_id}
    return render(request, 'summary/display_status.html', context)


@login_required
def add_status(request, user_id, contest_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    try:
        user.userprofile
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('users:modify_profiles'))
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:index'))
    if request.method != 'POST':
        form = StatusForm(contest_id=contest_id, user_id=user_id)
    else:
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=request.POST)
        if form.is_valid():
            # convert string from fields to ac_status and contributor
            ac_s = []
            ctb = []
            for key, value in form.cleaned_data.items():
                if key[0] == 'p':
                    ac_s.append(value)
                elif key[0] == 'c':
                    ctb.append(str(strlist_to_int(value, 1)))
            # complete the status
            status = form.save(commit=False)
            status.owner = user.userprofile
            status.contest = cts
            status.ac_status = strlist_to_int(ac_s, 4)
            status.contributor = strlist_to_int(ctb, 8)
            status.save()
            return HttpResponseRedirect(reverse(
                'summary:display_status',
                args=[user_id, contest_id]
            ))

    context = {'user_handle': user, 'contest': cts, 'form': form}
    return render(request, 'summary/add_status.html', context)


@login_required
def edit_status(request, user_id, contest_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:index'))
    status = Status.objects.get(owner=user.userprofile, contest=cts)
    if request.method != 'POST':
        ac_s = int_to_strlist(status.ac_status, 4, cts.num_of_problem)
        ctb = ctblist_to_strlist(int_to_strlist(status.contributor, 8, cts.num_of_problem))
        initial_value = {}
        initial_value['summary'] = status.summary
        for i in range(0, cts.num_of_problem):
            initial_value['p' + str(i)] = ac_s[i]
            initial_value['c' + str(i)] = ctb[i]
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=initial_value)
    else:
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=request.POST)
        if form.is_valid():
            # convert string from fields to ac_status and contributor
            ac_s = []
            ctb = []
            for key, value in form.cleaned_data.items():
                if key[0] == 'p':
                    ac_s.append(value)
                elif key[0] == 'c':
                    ctb.append(str(strlist_to_int(value, 1)))
            # rewrite the status
            status.summary = form.cleaned_data['summary']
            status.ac_status = strlist_to_int(ac_s, 4)
            status.contributor = strlist_to_int(ctb, 8)
            status.save()
            return HttpResponseRedirect(reverse(
                'summary:display_status',
                args=[user_id, contest_id]
            ))

    context = {'user_handle': user, 'contest': cts, 'form': form}
    return render(request, 'summary/edit_status.html', context)
