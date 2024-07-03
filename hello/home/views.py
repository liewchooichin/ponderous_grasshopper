from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, Engine
from django.utils import safestring, html


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
    """News of the website"""
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

def experiment_escape(request):
    """Turning escape on and off"""
    engine = Engine.get_default()
    engine.get_default()
    #t = engine.get_template("experiment.html")
    # Using default auto-escape of the engine. This is without the mark_safe.
    #data = {"instrument": "<b>tuba</b> --> <-- <b>baritone</b>"}
    # This is with mark_safe. mark_safe can only be used with individual string.
    #value = safestring.mark_safe("<b>tuba</b> --> <br> <-- <b>baritone</b> <br> trumpet")
    #data = {"instrument": value}
    # Using html.format_html to mark a chunk of html content.
    name = "French horn"
    value = html.format_html("big <i>{}</i>", name)
    data = {"instrument": value}
    return render(request=request, template_name="experiment.html" , context=data)

    