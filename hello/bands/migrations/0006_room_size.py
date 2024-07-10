# Generated by Django 5.0.4 on 2024-07-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0005_alter_bandgroup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='size',
            field=models.CharField(choices=[('L', 'Large--Up to 200 people'), ('M', 'Medium--Up to 100 people'), ('S', 'Small--Up to 50 people')], default='S', max_length=1, verbose_name='Capacity of room'),
        ),
    ]