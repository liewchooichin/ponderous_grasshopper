from django.shortcuts import render

# added by me
from datetime import datetime

def index(request):
    context = {
        "title": "Octocat",
        "today": str(datetime.today()),
    }
    return render(request, "hello_index.html", context)