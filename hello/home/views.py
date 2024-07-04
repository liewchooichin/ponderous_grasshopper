from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, Engine
from django.utils import safestring, html

from datetime import date, timedelta

# Global variable for index page
# These are common Home and navigation bar names.
# I put in in one place so that any changes to the
# navigation bar do not have to change the key-value
# data in each view.
global index_data
index_data = {
    "title": "Home",
    "brand": "RiffMates",
    "homepage": "hello_view",
    "credits": "credits",
    "about": "about",
    "urls": [
        ("news", "News"), 
        ("experiment_escape", "Experiment"),
    ],
}


# Definition of views
def credits(request):
    """Return the credits message"""
    content = "Credits: Django in Action"
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
    # get the date
    today = date.today()
    before1 = today - timedelta(days=1)
    before2 = today - timedelta(weeks=1)
    before3 = today - timedelta(weeks=2)
    # compose the data for context
    data = index_data
    data.update({
        'news': [
            (today, 'RiffMates now has a base page with Bootstrap.'),
            (before1, 'RiffMates has its first views and templates.'),
            (before2, 'RiffMates has just created its first Django app.'),
            (before3, 'Following a quick run through tutorial of Django in MDN.'),
        ],
        'title': "News",
    })
          
    return render(request=request,
                  template_name='news2.html', 
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

    
def starter_bootstrap(request):
    """Bootstrap starter sample"""
    return render(request=request, template_name="starter_bootstrap.html", context={})

def index(request):
    """Base html with starter Bootstrap sample"""
    # Use the global index_data. If there is anything that is specific
    # to the index page, then update the data (local variable) here.
    data = index_data
    return render(request=request, template_name="base.html", context=data)