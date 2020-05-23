from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request, 'homepage/landing_page.html')


def landing_page(request):
    return render(request, 'homepage/new_landing_page.html')
