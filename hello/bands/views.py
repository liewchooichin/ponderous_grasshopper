# hello/bands/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

# Create your views here.
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.views import generic

from bands.models import Musician, Venue, Room, BandGroup
from bands.forms import RoomForm, VenueForm
from home import views, page_util

# Pagination utilities

# import the global variables on the startup page
data = views.index_data


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
  
    # Call the shared page util function to get the
    # number of items_per_page
    #items_per_page = page_util._get_items_per_page(request)
    # manually set the items per page
    items_per_page = 3
    # A page with n objects per page 
    paginator = Paginator(all_musicians, items_per_page)
    # Calss the shared function to get the page number
    page_num = page_util._get_page_num(request, paginator)
    page = paginator.page(page_num)

    data.update({
        'title': 'Musicians list',
        'total_pages': paginator.num_pages,
        'musicians': page.object_list,
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


# Require login to view venues
# This is using user_passes_test function.
def has_venue(user):
    """
    Anonymous users have no profile, which triggers an AttributeError.
    Check how many venues the user controls. If it is one or more, 
    allow them in.
    """
    try:
        venue_count = user.userprofile.venues_operated.count()
        if venue_count > 1:
            return True
        else:
            return False
    except AttributeError as err:
        print(f"AttributeError: {err}")
        return False

#@user_passes_test(has_venue)
@login_required
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


# Restricted page that users require login
@login_required
def restricted_page(request):
    data = {
        'title': 'Restriced page',
        'content': '<h1>Members only</h1>',
    }
    return render(request=request, 
                  template_name="restricted_page.html",
                  context=data)

# Login and authorization is for Musician only
# Raise django.http.Http404 exception for not allowed access
@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    # request.user is the authenticated user, and userprofile
    # is the reverse relationship to the UserProfile ORM model.
    profile = request.user.userprofile
    # set to True if authorization succeeds.
    allowed = False

    # musician_profile is defined in the models.UserProfile
    if profile.musician_profiles.filter(
        id=musician_id).exists():
        allowed = True
    else:
        # User is not this musician, check if they are a band mate
        # Store all the user's associated Musician objects as a set.
        musician_profiles = set(
            profile.musician_profiles.all()
        )
        for b in musician.bandgroup_set.all():
            band_musicians = set(b.musicians.all())
            # intersection() is a method of set
            if musician_profiles.intersection(band_musicians):
                allowed = True
                break
        
    # if not allowed, raise an error
    if not allowed:
        raise Http404("Permission denied")

    # fill in the return context
    content = f"""
        <h1>Musician page: {musician.first_name} 
            {musician.last_name}</h1>
        <p>Musician's top budget practicing venues for rental.</p>
    """
    data = {
        'title': 'Musician restricted',
        'content': content,
    }
    return render(request, "restricted_page.html", data)

#login_required
def venue_edit(request, venue_id=0):
    """"Add or edit a venue according to the venue_id.
        If venue_id==0, add a room, else edit a room.
    """
    print(f"\t{request.user.email}")
    print(f"\t {request.user} ({request.user.id})")

    # Check is it an edit or add?
    # Check if the requested Venue object is part of the
    # user's venues_operated relationship. If not, raise
    # a 404 error.
    if venue_id != 0:
        # Fetch the requested Venue object
        venue = get_object_or_404(Venue, id=venue_id)
        print(f"\t{venue}")
        venues_operated_by_current_user = \
            request.user.userprofile.venues_operated.filter(
                id=venue_id
            )
        
        if not venues_operated_by_current_user.exists():
            raise Http404("A user can only edit controlled venues.")
    
    # GET
    if request.method == "GET":
        if venue_id == 0:
            form = VenueForm()
        else:
            form = VenueForm(instance=venue)
    # POST
    elif request.method == "POST":
        if venue_id == 0:
            # Add a venue: create a new empty Venue object
            # associated with the form.
            venue = Venue.objects.create()
        
        # include request.FILES in form creation to get
        # both the form's fields and the uploaded files.
        form = VenueForm(data=request.POST, files=request.FILES,
                         instance=venue)

        # If Add venue, add the venue to the user's venues_operated
        # relationship.
        if form.is_valid():
            venue = form.save(commit=False)
            # Save the venue operator to the current user
            #owner = venue.
            # Add the venue to the user's profile
            request.user.userprofile.venues_operated.add(venue)
            request.user.userprofile.user = request.user
            return redirect("venues_list")
        
    # Was a GET, or Form was not valid
    data = {
        'title': 'Edit or add venue',
        'form': form,
    }
    
    return render(request=request, 
                  template_name="venue_edit.html", context=data)



