"""
This module contains the views for the app.
"""

from django.shortcuts import render


# Create a dummy function
def home(request):
    return render(request, 'home.html')
