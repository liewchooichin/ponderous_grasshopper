from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def credits(request):
    content = "Django in Action"

    return HttpResponse(content=content, content_type="text/plain")
    