# hello/bands/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# Create your views here.

from bands.models import Musician, Venue, Room, BandGroup
from home import views  
# Pagination utilities

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
    all_musicians = Musician.objects.all().order_by("first_name")
    # A page with 2 objects per page 
    paginator = Paginator(all_musicians, 1)

    # GET the page from query string. 
    # If the key page does not exists, default to 1.
    page_num = request.GET.get('page', 1)
    page_num = int(page_num)
    # Check the page range
    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages
    # Fetch the page object containing the subsets of items
    page = paginator.page(page_num)

    data.update({
        'title': 'Musicians list',
        'musicians': page.object_list,
        'page': page,
    })
    return render(request=request, template_name="musicians_list.html", context=data)
