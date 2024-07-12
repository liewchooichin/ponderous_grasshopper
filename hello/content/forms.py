# App content

from django import forms


class CommentForm(forms.Form):
    """Forms for user to enter comment"""
    name = forms.CharField(max_length=100, 
                           label="Name", 
                           initial="",
                           show_hidden_initial=True)
    email = forms.EmailField(max_length=100,
                             label="Email",
                             required=False,
                             empty_value="No email",
                             initial="",
                             show_hidden_initial=True)
    subject = forms.CharField(max_length=160, 
                              label="Subject", 
                              initial="",
                              show_hidden_initial=True)
    comment = forms.CharField(
        max_length=300,
        label="Comments",
        initial="",
        help_text="Input your comment here. Max length: 300 characters",
        show_hidden_initial=True,
        widget=forms.Textarea(
            attrs = {"rows": "6", "cols": "50"}
        ),
    )

