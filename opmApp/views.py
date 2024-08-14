from django.shortcuts import render
from .models import *



def home(request):
    
    
    return render(request,"temp/home.html")



def error_404(request, exception):
    return render(request, '404/404.html', status=404)