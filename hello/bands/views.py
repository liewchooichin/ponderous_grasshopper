# hello/bands/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# Create your views here.
from django.utils.html import format_html
from django.urls import reverse

from bands.models import Musician, Venue, Room, BandGroup
from home import views, page_util

# Pagination utilities

# import the global variables on the startup page
data = views.index_data



# Views of bands
def musician_detail(request, musician_id):
    """Individual musician data"""
    musician = get_object_or_404(Musician, id=musician_id)

    # show bandgroup
    def show_bandgroup(obj):
        bandgroup = obj.bandgroup_set.all()

        if len(bandgroup) == 0:
            return format_html("<i>None</i>")

        return bandgroup
    show_bandgroup.short_description = "Band groups"

    # context
    data.update({
        "title": "Musician detail",
        "musician": musician,
        "style": Musician.STYLE_MUSIC.get(musician.style, ""),
        "bandgroup": show_bandgroup(musician),
    })
    return render(request=request, template_name="musician_detail.html", context=data)

def musicians_list(request):
    """List of musicians"""
    all_musicians = Musician.objects.all().order_by("first_name")
    
    # show bandgroup
    def show_bandgroup(obj):
        bandgroup = obj.bandgroup_set.all()

        if len(bandgroup) == 0:
            return format_html("<i>None</i>")
        
        # create a html band_name_list
        band_name_list = format_html("")
        for b in bandgroup:
            url = reverse("bandgroup_detail", kwargs={"bandgroup_id": b.id})
            band_name = format_html(
                "<li class='list-group-item'><a href='{}'>Band: {}</a></li>", url, b.name)
            band_name_list += band_name

        return band_name_list
    show_bandgroup.short_description = "Band groups"

    # Call the shared page util function to get the
    # number of items_per_page
    items_per_page = page_util._get_items_per_page(request)
    # A page with n objects per page 
    paginator = Paginator(all_musicians, items_per_page)
    # Calss the shared function to get the page number
    page_num = page_util._get_page_num(request, paginator)
    page = paginator.page(page_num)

    # for each object in the page, show the bandgroup
    def get_bandgroup_for_each_musician():
        page_bandgroup_list = []
        for i in range(items_per_page):
            bandgroup_list = format_html("<ul class='list-group'>")
            for obj in page.object_list:
                # format the names in ul
                bandgroup_list = show_bandgroup(obj)
            bandgroup_list += format_html("</ul>")
        page_bandgroup_list.append(bandgroup_list)
        return page_bandgroup_list

    # put the musician and her bandgroup in ul
    #def format_bandgroup_list():
        #bandgroup_list = format_html("<ul class='list-group'>")

    data.update({
        'title': 'Musicians list',
        'musicians': page.object_list,
        'bandgroup': get_bandgroup_for_each_musician(),
        'page': page,
    })
    return render(request=request, template_name="musicians-list.html", context=data)


def bandgroup_detail(request, bandgroup_id):
    """Detail of a particular band group"""
    bandgroup = get_object_or_404(BandGroup, id=bandgroup_id)
    data.update({
        'title': 'Band group detail',
        'bandgroup': bandgroup,
    })
    
    return render(request=request, 
                  template_name='bandgroup_detail.html',
                  context=data)


def bandgroups_list(request):
    """List of all band groups in the site"""
    all_bandgroups = BandGroup.objects.all().order_by("name")
    items_per_page = page_util._get_items_per_page(request)
    paginator = Paginator(all_bandgroups, items_per_page)
    page_num = page_util._get_page_num(request, paginator)
    page = paginator.page(page_num)

    data.update({
        'title': 'Band groups list',
        'bandgroups': page.object_list,
        'page': page,
    })

    return render(request=request, 
                  template_name="bandgroups_list.html", 
                  context=data)


# Venues and rooms
def room_detail(request, room_id):
    """Detail of a room"""
    room = get_object_or_404(Room, id=room_id)
    data.update({
        'title': 'Room details',
        'room': room,
    })

    return render(request=request,
                  template_name="room_detail.html",
                  context=data)

def venues_list(request):
    """List of all venues in the site"""
    all_venues = Venue.objects.all().order_by("name")
    items_per_page = page_util._get_items_per_page(request)
    paginator = Paginator(all_venues, items_per_page)
    page_num = page_util._get_page_num(request, paginator)
    page = paginator.page(page_num)

    data.update({
        'title': 'List of venues',
        'venues': page.object_list,
        'page': page,
    })

    return render(request=request,
                  template_name="venues_list.html",
                  context=data)
