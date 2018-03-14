from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth import get_user


def index(request):
	return HttpResponseRedirect(reverse('summary:index'))