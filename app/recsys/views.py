"""
This module contains the views for the recsys app.
"""

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'recsys/index.html')
