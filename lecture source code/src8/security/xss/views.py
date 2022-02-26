from django.shortcuts import HttpResponse, render

# Create your views here.
def index(request, path):
    return HttpResponse(f"Requested Path: {path}")
