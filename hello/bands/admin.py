from typing import Any
from django.contrib import admin

# For UserProfile through the DjangoAdmin
from django.contrib import auth

# Register your models here.

# Import utility classes
from datetime import datetime, date
from django.utils.html import format_html, mark_safe, format_html_join
from django.urls import reverse
from django.db.models.query import QuerySet

# Import my models
from bands.models import Musician, BandGroup, Venue, Room
# UserProfile
from bands.models import UserProfile

# Make a custom list filter based on decades
class DecadeListFilter(admin.SimpleListFilter):
    """Filter birth year of musician by every decades"""
    # This is the title of the list filter
    title = 'decade born'
    # This is the list filter's query parameter name
    parameter_name = 'decade'

    def lookups(self, request, model_admin) -> list[tuple[Any, str]]:
        """
        Returns a list of tuples. 
        The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. 
        The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        result = []
        this_year = datetime.today().year
        # Determine the current decade
        # For example, 1990=>1990, 1991=>1990.
        this_decade = (this_year//10) * 10
        start = this_decade - 10
        # Loop backward through the 10 previous decades
        for year in range(start, start-100, -10):
            # Add a tuple (key, value) containing the base
            # year of the decade and a display string.
            result.append((str(year), f"{year}-{year+9}"))
        
        return result

    def queryset(self, request, queryset) -> QuerySet[Any] | None:
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        self.value().
        """
        # Get the filtered value, checking for None (meaning no filter)
        start = self.value()
        if start is None:
            return queryset
        
        # Run a subfilter on the QuerySet, restricting the birth field to
        # the chosen decade, starting on Jan 1 (starting 0 decade) 
        # to 31 Dec (9 years laster)
        start = int(start)
        result = queryset.filter(
            birth__gte = date(start, 1, 1),
            birth__lte = date(start+9, 12, 31),
        )
        
        return result

# Use the register() function as a class decorator
# to associate the admin class with the model.

# The classes here inherits the admin.ModelAdmin
@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    """Admin page for musician"""
    # List the properties to be displayed
    list_display = ("id", "first_name", "last_name", "birth", 
                    "show_weekday", "show_bandgroups", "style")
    # Example of searches: __startswith, __exact
    search_fields = ("first_name__startswith", "last_name")
    # Filter is best used with choices
    list_filter = ("style", DecadeListFilter, "bandgroup__name")

    # show_weekday can be implemented on either the Musician
    # class or the admin.ModelAdmin class.
    # Let's say I only want this feature show_weekday to be
    # in the Django Admi, it is a best practice to it in
    # the MusicianAdmin class instead.
    # This callable function has an attribute. In Python,
    # a function can have attributes.
    # The attribute short_description will become the name
    # of the column title in the admin view.
    def show_weekday(self, obj):
        # Fetch weekday of artist's birth
        # The date format %A is for the weekday
        return obj.birth.strftime("%A")
    
    # Query all bands associated with this musician
    def show_bandgroups(self, obj):
        bandgroup = obj.bandgroup_set.all()
        if len(bandgroup) == 0:
            # This return can be formatted in html
            return format_html("<i>None</i>")
        
        # if there is more than one band
        plural = ""
        if len(bandgroup) == 1:
            plural = f" ({len(bandgroup)})"
        elif len(bandgroup) > 1:
            plural = "s" + f" ({len(bandgroup)})"
        
        # Query parameter using the __in suffix and a comma
        # separated list of Bandgroup id.
        # Look up the Bandgroup listing page, and then add
        # the query parameter to the end.
        query_param = "?id__in=" + ",".join([str(b.id) for b in bandgroup])
        url = reverse("admin:bands_bandgroup_changelist") + query_param
        # Create a safe <a> tag using the URL and the pluralization of Bandgroup
        result = format_html("<a href='{}'>Band{}</a>", url, plural)
        return result
    show_bandgroups.short_description = "Band groups"



    # customize the column title
    show_weekday.verbose_name = "Birth weekday"
    show_weekday.short_description = "Birth weekday"





@admin.register(BandGroup)
class BandGroupAdmin(admin.ModelAdmin):
    """Admin page for BandGroup"""
    list_display = ["name", "show_members_2"]
    #list_display = ["name"]
    search_fields = ["name__startswith"]
        # Query all bands associated with this musician
    
    # First method to show_members. This is the same as
    # the other show_xxx in the admin.py.
    # The second method is shown below.
    def show_members(self, obj):
        members = obj.members.all()
        if len(members) == 0:
            # This return can be formatted in html
            return format_html("<i>None</i>")
        
        # if there is more than one band
        plural = ""
        if len(members) == 1:
            plural = f" ({len(members)})"
        elif len(members) > 1:
            plural = "s" + f" ({len(members)})"
        
        # Query parameter using the __in suffix and a comma
        # separated list of Bandgroup id.
        # Look up the Bandgroup listing page, and then add
        # the query parameter to the end.
        query_param = "?id__in=" + ",".join([str(m.id) for m in members])
        # IMPORTANT: The reverse must take the model class name, for
        # example bands_musician, NOT bands_members.
        url = reverse("admin:bands_musician_changelist") + query_param
        # Create a safe <a> tag using the URL and the pluralization of Bandgroup
        result = format_html("<a href='{}'>Member{}</a>", url, plural)
        return result
    show_members.short_description = "Members"

    # Another way to show_members_2
    def show_members_2(self, obj):
        members = obj.members.all()
        
        url = reverse("admin:bands_musician_changelist")

        # format the link in a list
        musician_link = format_html("<ul class='list-group'>")
        for m in members:
            query_param = f"?id={m.id}"
            musician_name = f"{m.first_name} {m.last_name}"
            member_list = format_html(
                "<li class='list-group-item'>"
                + f"<a href='{url}{query_param}'>{musician_name}</a>"
                + "</li>"
            )
            musician_link += member_list
        # append the closing </ul>
        musician_link += format_html("</ul>")
        return musician_link
    
    # Give the column a name
    show_members_2.short_description = "Members"
    

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Admin page for Venue"""
    list_display = ["name", "show_rooms"]
    search_fields = ["name"]

    def show_rooms(self, obj):
        rooms = obj.room_set.all()
        if len(rooms) == 0:
            return format_html("<i>None</i>")
        
        # format the rooms string
        plural = ""
        if len(rooms) == 1:
            plural = f" ({len(rooms)})"
        elif len(rooms) > 1:
            plural = "s" + f" ({len(rooms)})"

        # Get the query parameters
        query_param = "?id__in=" + ",".join([str(r.id) for r in rooms])
        url = reverse("admin:bands_room_changelist") + query_param
        result = format_html("<a href='{}'>Room{}</a>", url, plural)
        return result
    show_rooms.short_description = "Rooms"
    

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin page for Room"""
    list_display = ["name", "size"]
    """Facets:
    Displaying the facet information means extra queries 
    to the database because the Django Admin has to look 
    up the count of each filter. This is why the NEVER option 
    is available, so you can turn it off if the query is too 
    expensive for your page.
    """
    #show_facets = admin.ShowFacets.ALWAYS
    #show_facets = admin.ShowFacets.NEVER
    # Show facet counts when the _facets query string
    # parameter is provided. For example,
    # http://localhost:8000/admin/bands/room/?_facets=True
    # This query is sent in Request when clicking on "Show counts"
    show_facets = admin.ShowFacets.ALLOW
    list_filter = ["size"]
    search_fields = ["name__startswith"]


# UserProfile
class UserProfileInline(admin.StackedInline):
    """
    Create a form by inheriting from admin.StackedInline
    Associate the stacked inline form with the UserProfile 
    object.
    """
    model = UserProfile
    can_delete = False

class UserAdmin(auth.admin.UserAdmin):
    """Use the new UserProfileInline class as a stacked form."""
    inlines = [UserProfileInline]

# Remove the old admin object for the User, and add the UserAdmin
# as its replacement.
admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)

