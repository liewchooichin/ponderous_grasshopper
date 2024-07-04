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
    def __str__(self):
        return f"Musician(id={self.id}, {self.first_name} {self.last_name})"
