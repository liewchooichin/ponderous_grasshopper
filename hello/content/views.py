# content/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.html import format_html

# for env variables
from decouple import config

# Create your views here.
from content.forms import CommentForm

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
