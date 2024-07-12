# App content

from django import forms


class CommentForm(forms.Form):
    """Forms for user to enter comment"""
    name = forms.CharField(max_length=100, label="Name", initial="Your name here")
    comment = forms.CharField(
        max_length=300,
        label="Your comments",
        initial="Tell us about your experience with the site",
        help_text="Input your comment here. Max length: 300 characters",
        widget=forms.Textarea(
            attrs = {"rows": "6", "cols": "50"}
        ),
    )

