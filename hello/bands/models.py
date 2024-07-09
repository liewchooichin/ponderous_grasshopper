from django.db import models

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
    
    def __str__(self):
        return f"BandGroup(id={self.id}, name={self.name})"