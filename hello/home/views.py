from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse

def credits(request):
    """Return the credits message"""
    content = "Django in Action"

    return HttpResponse(content=content, content_type="text/plain")
    

def about(request):
    """Return the about message"""
    content ="About this project"
    return HttpResponse(content=content, content_type="text/plain")

def version(request):
    """Version of the app"""
    data = {"version": "0.0.1", }
    return JsonResponse(data=data)

def news(request):
    data = {
        'news': [
            'RiffMates now has a news page',
            'RiffMates has its first web page',
        ],
    }        
    return render(request=request,
                  template_name='news.html', 
                  context=data,
                 )