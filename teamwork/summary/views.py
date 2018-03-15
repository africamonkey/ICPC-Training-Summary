from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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
    context = {'status': status}
    return render(request, 'summary/display_status.html', context)


def add_status(request, user_id, contest_id):
    cts = get_object_or_404(Contest, pk=contest_id)
    user = get_user(request)
    if user.id != user_id:
        return HttpResponseRedirect(reverse('summary:display_status', args=[user_id, contest_id]))
    if request.method != 'POST':
        form = StatusForm(contest_id=contest_id, user_id=user_id)
    else:
        form = StatusForm(contest_id=contest_id, user_id=user_id, data=request.POST)
        if form.is_valid():
            status = Status.objects.create(owner=user.userprofile, contest=cts)
            status.summary = form.cleaned_data["summary"]
            t = []
            for key, value in form.cleaned_data.items():
                if key[0] == 'p':
                    t.append(value)
            status.ac_status = strlist_to_int(t, 4)
            status.save()
            return HttpResponseRedirect(reverse(
                'summary:display_status',
                args=[user_id, contest_id]
            ))

    context = {'user_handle': user, 'contest': cts, 'form': form}
    return render(request, 'summary/add_status.html', context)
