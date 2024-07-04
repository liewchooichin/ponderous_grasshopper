# hello/bands/views.py
from django.shortcuts import render, get_object_or_404

# Create your views here.

from bands.models import Musician
from home import views  

# import the global variables on the startup page
data = views.index_data

# Views of bands
def musician_detail(request, musician_id):
    """Individual musician data"""
    musician = get_object_or_404(Musician, id=musician_id)
    data.update({
        "title": "Musician detail",
        "musician": musician,
    })
    return render(request=request, template_name="musician_detail.html", context=data)

def musicians_list(request):
    """List of musicians"""
    musicians_list = Musician.objects.all().order_by("first_name")
    data.update({
        'title': 'Musicians list',
        'musicians': musicians_list,
    })
    return render(request=request, template_name="musicians_list.html", context=data)
