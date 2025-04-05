from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def home(request):
    context = {}
    return render(request, 'homePage.html', context)