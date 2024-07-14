from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from bands.models import Musician, BandGroup

# Create your models here.

# Use TextChoices class instead of the dict({"key": "value"})
class MusicianBandChoice(models.TextChoices):
    """Equivalent to 
        {"M": "MUSICIAN",
         "B": "BAND"}
    """
    MUSICIAN = "M"
    BAND = "B"

class SeekingAd(models.Model):
    # This field gets automatically populated with
    # the current date when the object gets created.
    id = models.SmallAutoField(primary_key=True)
    create_date = models.DateField(auto_now_add=True)
    # A foreign key of the user who owns the ad
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    seeking_choices = {
        "M": "MUSICIAN",
        "B": "BAND"
    }
    seeking = models.CharField(
        max_length=1,
        #choices=MusicianBandChoice.choices
        choices = seeking_choices,
    )
    # A musician seeking a band
    musician = models.ForeignKey(
        to=Musician,
        #choices=Musician,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    # A band seeking a musician
    band = models.ForeignKey(
        to=BandGroup,
        on_delete=models.SET_NULL,
        #choices=BandGroup,
        blank=True,
        null=True,
    )
    # Text to store the ads
    ads = models.TextField(
        max_length=300,
    )

    class Meta:
        ordering = ["-create_date"]

    def __str__(self):
        return f"SeekingAd(id={self.id}, owner={self.owner}({self.owner.id}))"
    
    def clean(self):
        """ (1) When seeking a musician, ensure the band field gets 
            populated and the musician field is empty.
            (2) When seeking a band, ensure the musician field gets
            populated and the band field is empty.
        """
        # Case (1)
        if self.seeking == MusicianBandChoice.MUSICIAN:
            # Validate seeking musician case
            if self.band is None:
                raise ValidationError(
                    "Band field is required when seeking a musician."
                )
            if self.musician is not None:
                raise ValidationError(
                    "Musician field should be empty for a band \
                    seeking a musician."
                )
        # Case (2)
        else:
            # Validate seeking band case
            if self.musician is None:
                raise ValidationError(
                    "Musician field is required when seeking a band."
                )
            if self.band is not None:
                raise ValidationError(
                    "Band field should be empty for a musician \
                    seeking a band."
                )

        super().clean() 