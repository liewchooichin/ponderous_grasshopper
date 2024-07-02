from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse

def credits(request):
    """credits(request)
    Return the credits message
    """
    content = "Django in Action"

    return HttpResponse(content=content, content_type="text/plain")
    

def about(request):
    """about(request)
    Return the about message
    """
    content ="About this project"
    return HttpResponse(content=content, content_type="text/plain")

def version(request):
    data = {"version": "0.0.1", }
    return JsonResponse(data=data)