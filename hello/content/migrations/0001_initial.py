# Generated by Django 5.0.4 on 2024-07-13 17:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bands', '0010_userprofile_alter_bandgroup_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeekingAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('seeking', models.CharField(choices=[('M', 'Musician'), ('B', 'Band')], max_length=1)),
                ('ads', models.TextField(max_length=200)),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bands.bandgroup')),
                ('musician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bands.musician')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['create_date'],
            },
        ),
    ]
