from django.shortcuts import render

__author__ = 'Michael'


def index(request):
    return render(request, 'admin_home.html', {})
