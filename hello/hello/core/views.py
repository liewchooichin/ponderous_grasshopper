from django.shortcuts import render

# added by me
from datetime import datetime

def index(request):
    context = {
        "title": "Django example",
        "today": str(datetime.today()),
    }
    return render(request, "index.html", context)