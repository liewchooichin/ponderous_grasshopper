#ModelForm

from django.forms import ModelForm
from .models import Musician, Venue, Room, BandGroup
from django.contrib.auth.decorators import login_required



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "venue", "size"]
    
    template_name = "form_template.html"
    