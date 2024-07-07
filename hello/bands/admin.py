from django.contrib import admin

# Register your models here.

# Import my models
from bands.models import Musician, BandGroup, Venue, Room

# Use the register() function as a class decorator
# to associate the admin class with the model.

# The classes here inherits the admin.ModelAdmin
@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    """Admin page for musician"""
    # List the properties to be displayed
    list_display = ("id", "first_name", "last_name", "show_weekday")

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
    
    # customize the column title
    show_weekday.short_description = "Birth weekday"
    


@admin.register(BandGroup)
class BandGroupAdmin(admin.ModelAdmin):
    """Admin page for BandGroup"""
    pass

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Admin page for Venue"""
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin page for Room"""
    pass
