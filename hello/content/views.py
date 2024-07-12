# content/views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Create your views here.
from content.forms import CommentForm

def comment(request):
    """Send users' comment to an admin's email"""
    if request.method == "GET":
        form = CommentForm()

    else: #POST
        form = CommentForm(request.POST)

        if form.is_valid():
            # Check content of cleaned_data
            for k, v in form.cleaned_data.items():
                print(f"Cleaned data: \n\t{k}: {v}")
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]

            message = f"""
                Received comment from {name}:\n\n
                {comment}
            """

            send_mail()


