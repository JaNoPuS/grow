"""
    MAIN VIEW DE GROWFOOD.CL
"""

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')