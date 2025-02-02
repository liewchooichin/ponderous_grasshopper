from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, Engine
from django.utils import safestring, html

from datetime import date, timedelta

# Global variable for index page
# These are common Home and navigation bar names.
# I put in in one place so that any changes to the
# navigation bar do not have to change the key-value
# data in each view.
global index_data
index_data = {
    "title": "Home",
    "brand": "RiffMates",
    "homepage": "hello_view",
    "credits": "credits",
    "about": "about",
    "urls": [
        ("bandgroups_list", "Band groups"),
        ("venues_list", "Venues"),
        ("venue_add", "Add a venue"),
        ("news", "News"), 
        ("experiment_escape", "Experiment"),
    ],
}


# Password reset
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode

from .forms import MyPasswordResetForm


# My own custome password reset handling view
# URL patterns for accounts: 
# https://docs.djangoproject.com/en/5.0/topics/auth/default/#using-the-views
def my_password_reset_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PasswordResetForm(request.POST) 
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # accounts/password_reset/done/ 
            # [name='password_reset_done']
            user_email = form.cleaned_data["email"]
            print("User email", user_email)
            # send email through Azure email client
            # reset link:
            # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
            protocol = "http"
            domain =  request.get_host()
            print("POST data")
            for k, v in request.POST.items():
                print(k, v)
            current_user = User.objects.filter(email=user_email)
            # for info
            email_view = PasswordResetView()
            print(email_view.get_template_names())

            # No idea how to get the uid and token
            uidb64 = "uidb64"
            token = "token"
            reset_link = (f"{protocol}://{domain}/accounts/reset/{uidb64}/{token}/")
            print(reset_link)
            password_reset_email = format_html(
            "<html>Please go to the following page and choose a new password: <a href='{}'>Reset password page</a></html>", reset_link
            )
            password_reset_subject = "Password reset request"
            from_email = "<DoNotReply@f0cf672a-d027-4901-bfea-018e517e7e1c.azurecomm.net>"
            print(password_reset_email)
            send_mail(subject=password_reset_subject,
              message=password_reset_email,
              from_email=from_email,
              recipient_list=[user_email],
              html_message=password_reset_email,
             )
            return HttpResponseRedirect(reverse('password_reset_done'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordResetForm()

    # password_reset_form: registration/password_reset_form.html
    return render(
                    request, 
                    "registration/password_reset_form.html", 
                    {"form": form}
                  )


# Definition of views
def credits(request):
    """Return the credits message"""
    #content = "Credits: Django in Action"
    #return HttpResponse(content=content, content_type="text/plain")
    data = index_data
    data.update({
        'title': 'Credits',
    })
    return render(request=request,
                  template_name="credits.html",
                  context=data)
    

def about(request):
    """Return the about message"""
    data = {"content": "About this project.\
        This is the simplest possible view in Django."}
    return render(request=request,
                  template_name="about.html", context=data)

def version(request):
    """Version of the app"""
    data = {"version": "0.0.1", }
    return JsonResponse(data=data)

def news(request):
    """News of the website"""
    # get the date
    today = date.today()
    before1 = today - timedelta(days=1)
    before2 = today - timedelta(weeks=1)
    before3 = today - timedelta(weeks=2)
    # compose the data for context
    data = index_data
    data.update({
        'news': [
            (today, 'RiffMates now has a new look with Bootstrap.'),
            (before1, 'RiffMates has its first views and templates.'),
            (before2, 'RiffMates has just created its first Django app.'),
            (before3, 'Following a quick run through tutorial of Django in MDN.'),
        ],
        'title': "News",
    })
          
    return render(request=request,
                  template_name='news2.html', 
                  context=data,
                 )

def experiment_escape(request):
    """Turning escape on and off"""
    engine = Engine.get_default()
    engine.get_default()
    #t = engine.get_template("experiment.html")
    # Using default auto-escape of the engine. This is without the mark_safe.
    #data = {"instrument": "<b>tuba</b> --> <-- <b>baritone</b>"}
    # This is with mark_safe. mark_safe can only be used with individual string.
    #value = safestring.mark_safe("<b>tuba</b> --> <br> <-- <b>baritone</b> <br> trumpet")
    #data = {"instrument": value}
    # Using html.format_html to mark a chunk of html content.
    name = "French horn"
    value = html.format_html("big <i>{}</i>", name)
    data = {"instrument": value}
    return render(request=request, template_name="experiment.html" , context=data)

    
def starter_bootstrap(request):
    """Bootstrap starter sample"""
    return render(request=request, template_name="starter_bootstrap.html", context={})

def index(request):
    """Base html with starter Bootstrap sample"""
    # Use the global index_data. If there is anything that is specific
    # to the index page, then update the data (local variable) here.
    data = index_data
    return render(request=request, template_name="base_index.html", context=data)

# New user signup
from home.forms import SignupForm
from django.shortcuts import redirect
from bands.models import Musician, Venue, UserProfile
from bands.models import User

def user_signup(request):
    """A form for new user to sign up to use the website"""
    if request.method == "GET":
        form = SignupForm()
    elif request.method == "POST":
        # create a new, empty User for the form
        #new_user = UserProfile.objects.create()
        #new_user = User.objects.create_user()
        form = SignupForm(
            data=request.POST,
        )
        # If form is valid, save the user
        if form.is_valid():
            ### for debugging
            for k, v in request.POST.items():
                print(f"{k}: {v}")
            
            new_user = User.objects.create_user(
                username=request.POST.get("username", ""),
                first_name = request.POST.get("first_name", ""),
                last_name = request.POST.get("last_name", ""),
                email=request.POST.get("email", ""),
                password=request.POST.get("password", ""),
            )
            new_user.is_staff = False
            new_user.is_active = True
            new_user.is_superuser = False
            new_user.date_joined = date.today()
            # Save a default user profile
            """
            profile = UserProfile()
            profile.id = len(UserProfile.objects.all()) + 1
            profile.user = new_user
            musician = Musician.objects.get(id=request.POST.get("musician_profiles", ""))
            venue = Venue.objects.get(id=request.POST.get("venues_operated", ""))
            profile.musician_profiles.add(musician)
            profile.venues_operated.add(venue)
            profile.save() # save the new profile
            """
            new_user.save() # save the new user
            form.save() # save the form
            #form.save_m2m() # save m2m
            

            # if signup is successful, redirect to login page.
            return redirect("login")
        else:
            print("form is not valid")
    # Was a GET or form is not valid
    data = {
        #"musician_profiles": Musician.objects.all(),
        #"venues_operated": Venue.objects.all(),
        "form": form,
    }
    return render(request=request,
                  template_name="user_signup.html",
                  context=data)

# Edit user profile
from home.forms import UserProfileEditForm
            
def edit_user_profile(request):
    """A view to update/edit user profile"""
    # Get the profile of the current user, if
    # the profile does not exists, create a new one.
    has_profile = hasattr(request.user, "userprofile")
    print(f"\tUser profile exists: {has_profile=}")

    if has_profile is True:
        profile = request.user.userprofile

    # GET
    if request.method == "GET":
        # print the profile for debug
        # if there is no profile, make a new form
        if has_profile is False:
            form = UserProfileEditForm()
        else:
            form = UserProfileEditForm(instance=profile)
    # POST
    elif request.method == "POST":
        if has_profile is False:
            profile = UserProfile.objects.create()
        
        form = UserProfileEditForm(data=request.POST,
                                   instance=profile)

        # if form is valid
        if form.is_valid():
            for k, v in request.POST.items():
                print(f"{k}: {v}")

            profile = form.save(commit=False)
            #request.user.userprofile.user = request.user
            musician = Musician.objects.get(
                id=request.POST.musician_profiles.id
            )
            print(f"\t{musician=}")
            venue = Venue.objects.get(
                id=request.POST.venues_operated.id
            )
            print(f"\t{venue=}")
            profile.save()
            print(f"\t{profile=}")
            # save many-to-many
            form.save_m2m()
            request.user.userprofile = profile
            return redirect("user_profile")

    # Was a GET or form is not valid
    if has_profile is True:
        musician_profiles = profile.musician_profiles.all()
        venues_operated = profile.venues_operated.all()
    else:
        musician_profiles = Musician.objects.all()
        venues_operated = Venue.objects.all()
    data = {
        "musician_profiles": musician_profiles, #Musician.objects.all(),
        "venues_operated": venues_operated, #Venue.objects.all(),
        "form": form,
    }
    return render(request=request,
                  template_name="edit_user_profile.html",
                  context=data)