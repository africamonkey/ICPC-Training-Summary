from django.shortcuts import render

def index(request):
    return render(request, 'index_page/index.html')

def about(request):
    return render(request, 'index_page/about.html')