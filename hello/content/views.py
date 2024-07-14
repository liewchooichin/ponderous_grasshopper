# content/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import views
from django.contrib.auth.models import User

# for env variables
from decouple import config

# Create your views here.
from content.forms import CommentForm, SeekingAdForm
from content.models import MusicianBandChoice, SeekingAd


def comment_form(request):
    """Send users' comment to an admin's email"""
    if request.method == "GET":
        form = CommentForm()

    else: #POST
        form = CommentForm(request.POST)

        if form.is_valid():
            # Check content of cleaned_data
            for k, v in form.cleaned_data.items():
                print(f"Cleaned data: \n\t{k}: {v}")
            user_name = form.cleaned_data["name"]
            user_email = form.cleaned_data["email"]
            user_subject = form.cleaned_data["subject"]
            user_comment = form.cleaned_data["comment"]

            message = f"""
                <html><body>
                <p>Details of the user comment:</p>
                <ul>
                    <li>Username: {user_name} </li>
                    <li>Email: {user_email} </li>
                    <li>Subject: {user_subject}</li>
                    <li>Comment: {user_comment} </li>
                </ul>
                </body></html>
            """
            html_message = format_html(message)
            
            from_email = config("AZURE_FROM_EMAIL", "")

            subject = "Comments from users"
            recipient_list = [user_email]

            send_mail(
                subject=subject,
                message=message,
                html_message=html_message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            
            return redirect("comment_done")
        
    # If form is not valid
    # Was a GET, or Form was not valid
    # This is the rendering part of the view, used in both
    # the GET and the POST if the form is not valid
    data = {
        "title": "Comment form",
        "form": form
        }
    
    
    return render(request=request, 
                  template_name="comment_form.html", 
                  context=data
                  )    


def comment_done(request):
    """
    The view to display when the comment form is valid and 
    submitted.
    """
    message = format_html("""
    <h1>Thank you for submitting your comment</h1>
    <p>Only constructive comment will be considered. <br>
        Thank you for your time.
    </p>
    """)
    data = {
        "title": "comment done",
        "message": message,
    }
    return render(request=request, 
                  template_name="comment_done.html",
                  context=data
                  )


# Classified Ads listing page
def ads_listing(request):
    data = {
        'seeking_musician': SeekingAd.objects.filter(
            seeking=MusicianBandChoice.MUSICIAN
        ),
        'seeking_band': SeekingAd.objects.filter(
            seeking=MusicianBandChoice.BAND
        ),        
    }

    return render(request=request,
           template_name="ads_listing.html",
           context=data)

def user_edit_ads(request):
    """A user can edit their own ads"""
    # Get the user id of the current request.user
    current_user = User.objects.get(username=request.user)
    print(f"\t{request.user=} {current_user.id} {current_user.username}")
    data = {
        'ad': SeekingAd.objects.filter(owner=current_user.id)
    }

    return render(request=request,
           template_name="user_edit_ads.html",
           context=data)


@login_required
# View to submit an ads by a user
def put_an_ads(request, ad_id=0):
    """A user can use this view to put a classified ads"""
    # GET
    if request.method == "GET":
        """And id of 0 indicates a new model object should be
        created, otherwise in Edit mode, the view looks up
        the existing SeekingAd object. The query requires both
        the id and the owner."""
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id,
                                   owner=request.user)
            form = SeekingAdForm(instance=ad)
    
    # POST
    elif request.method == "POST":
        """An id of 0 means that the form is created based solely on 
        the submitted data. """
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id,
                                   owner=request.user)
            form = SeekingAdForm(request.POST, instance=ad)

        if form.is_valid():
            ad = form.save(commit=False)
            # The owner will be automatically determined
            # from the user who login to the site.
            ad.owner = request.user
            ad.save()
            return redirect("ads_listing")
    
    # GET or form is not valid
    data = {
        'title': "Put an ads",
        'form': form,
    }
    return render(request=request, 
                  template_name="put_an_ads.html",
                  context=data)


# Using generic views
class SeekingAdsGenericCreateView(views.generic.edit.CreateView):
    model = SeekingAd
    fields = ["owner", "seeking",
              "musician", "band", "ads"]
    
    #default template at content/templates/content/seekingad_form.html
    success_url = "/content/ads_listing/"

class SeekingAdsGenericUpdateView(views.generic.edit.UpdateView):
    model = SeekingAd
    fields = ["seeking",
              "musician", "band", "ads"]
    #default template at content/templates/content/seekingad_form.html
    #success_url = reverse(viewname="ads_listing.html")
    success_url = "/content/ads_listing/"

class SeekingAdsGenericDeleteView(views.generic.edit.DeleteView):
    model = SeekingAd
    fields = ["seeking",
              "musician", "band", "ads"]
    #default template at content/templates/content/seekingad_confirm_delete.html
    success_url = "/content/seekingad_delete_successful/"

def seekingad_delete_successful(request):
    """Display after successful deletion"""
    data = {
        'title': 'Delete successful',
        'user': request.user,
        'ads_id': "some id",
    }
    return render(request=request, 
                  template_name="seekingad_delete_successful.html",
                  context=data)