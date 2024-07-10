# Generated by Django 5.0.4 on 2024-07-10 12:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0009_alter_bandgroup_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='bandgroup',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='musician',
            options={'ordering': ['first_name']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Room'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Venue'),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('name', 'venue')},
        ),
        migrations.AddIndex(
            model_name='venue',
            index=models.Index(fields=['name'], name='bands_venue_name_b37d47_idx'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='musician_profiles',
            field=models.ManyToManyField(blank=True, to='bands.musician'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='venues_operated',
            field=models.ManyToManyField(blank=True, to='bands.venue'),
        ),
    ]
