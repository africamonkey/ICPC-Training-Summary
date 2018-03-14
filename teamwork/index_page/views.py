from django.shortcuts import render

def index(request):
    return render(request, 'index_page/index.html')

def test(request):
    return render(request, 'index_page/base.html')
