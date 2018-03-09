from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth import logout

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('contests:index'))
