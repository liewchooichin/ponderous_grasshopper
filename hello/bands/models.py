from django.db import models

# for user profile class
from django.contrib.auth.models import User
# Signal to handle when there is a login failure
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.dispatch import receiver


# Create your models here.

class Musician(models.Model):
    """Musician's info"""
    id = models.SmallAutoField(
        primary_key=True,
    )
    first_name = models.CharField(
        verbose_name="First name",
        max_length=50,
        help_text="First name",
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=50,
        help_text="Last name",
    )
    birth = models.DateField(
        verbose_name = "Date of birth",
    )
    # choices of music
    STYLE_MUSIC = {
        "ROCK": "Rock and roll",
        "RELA": "Relaxing",
        "LIVE": "Lively",
    }
    style = models.CharField(
        verbose_name="Style of music",
        max_length=4,
        choices=STYLE_MUSIC,
        default="RELA", 
        help_text="Main style of music",
    )

    # Meta
    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return f"Musician(id={self.id}, {self.first_name} {self.last_name})"

# Venue and Room models and their one-to-many relationship

class Venue(models.Model):
    """One venue can have many rooms, but a room can only belong to one venue."""
    """A venue table can list a unique venue."""
    """The unique Venue id will be a foreign key in the Room table."""
    """The Room table has a unique room. Each row of unique room"""
    """will be associated with a Venue through the Venue foreign key."""
    """If a venue gets removed from the database, it doesn’t"""
    """make sense to keep the associated rooms, so the on_delete value for""" 
    """the Room is CASCADE."""
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Venue")

    # Meta
    class Meta:
        ordering =["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"Venue (id={self.id}, name={self.name})"
    
class Room(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Room")
    venue = models.ForeignKey("Venue", on_delete=models.CASCADE)

    # properties 
    SIZE = {
        'L': "Large--Up to 200 people",
        'M': "Medium--Up to 100 people",
        'S': "Small--Up to 50 people",
    }
    size = models.CharField(
        verbose_name="Capacity of room", 
        choices=SIZE, 
        max_length=1, 
        default="S")

    # Meta
    class Meta:
        ordering = ["name"]
        # can add indexes
        # unique_together
        # Notice that unique_together is [[]] list of list.
        # If there are more attributes, than the list of list can
        # be used to specify many different set of uniqueness.
        unique_together = [["name", "venue"]]

    def __str__(self):
        return f"Room(id={self.id}, name={self.name})"

# Many-to-many relationship between bands and musicians
# A musician can belong to many groups.
# A group can have many musician.
# It doesn’t matter which model has the ManyToManyField, but you should 
# only put it in one of the models – not both.
class BandGroup(models.Model):
    """A group can have many musicians. Many-to-many relationship."""
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, default="Band Group", verbose_name="Band group")
    members = models.ManyToManyField(to="bands.Musician", verbose_name="Members")
    
    # Meta
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"BandGroup(id={self.id}, name={self.name})"
    
# UserProfile
class UserProfile(models.Model):
    """
    Create a one-to-one relationship between UserProfile and User.
    A user can be both a musician and a venue operator. 
    Create many-to-many relationships with Musician and Venue objects.
    Store relationships between this user account and any Musician or
    Venue objects.
    Set blank=True so these can be empty fields in the DjangoAdmin
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    musician_profiles = models.ManyToManyField(Musician, blank=True)
    venues_operated = models.ManyToManyField(Venue, blank=True)

    def __str__(self):
        return (f"UserProfile: {self.user}")


# Track user login using signals
@receiver(user_login_failed)
def track_login_failure(sender, **kwargs):
    """
    The user_login_failed signal includes credential
    information and the request object in its keyword
    argument dictionary.
    """
    for k, v in kwargs.items():
        print(k, v)
    username = kwargs["credentials"]["username"]
    url = kwargs["request"].path
    print(f"Login failure: \n\tUser: {username} \n\tPath: {url}")

# Logout info

# Track user login using signals
@receiver(user_logged_out)
def track_logged_out(sender, **kwargs):
    """
    The user_login_failed signal includes credential
    information and the request object in its keyword
    argument dictionary.
    """
    for k, v in kwargs.items():
        print(k, v)
    username = kwargs["user"]
    url = kwargs["request"].path
    print(f"Logout: \n\tUser: {username} \n\tPath: {url}")

# Track user login using signals
@receiver(user_logged_in)
def track_logged_in(sender, **kwargs):
    """
    The user_login_failed signal includes credential
    information and the request object in its keyword
    argument dictionary.
    """
    
    for k, v in kwargs.items():
        print(k, v)
    username = kwargs["user"]
    url = kwargs["request"].path
    print(f"Logout: \n\tUser: {username} \n\tPath: {url}")