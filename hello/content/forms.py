# App content

from django import forms


class CommentForm(forms.Form):
    """Forms for user to enter comment"""
    name = forms.CharField(max_length=100, 
                           label="Name", 
                           initial="",
                           show_hidden_initial=True,
                           help_text="Your name")
    email = forms.EmailField(max_length=100,
                             label="Email",
                             required=False,
                             empty_value="No email",
                             initial="",
                             show_hidden_initial=True,
                             help_text="Your email")
    subject = forms.CharField(max_length=10, 
                              label="Subject", 
                              initial="",
                              show_hidden_initial=True,
                              help_text="The subject of the comment")
    comment = forms.CharField(
        max_length=10,
        label="Comments",
        initial="",
        help_text="Max length: 300 characters",
        show_hidden_initial=True,
        widget=forms.Textarea(
            attrs = {"rows": "6", "cols": "50"}
        ),
    )
    # Use custom form template
    template_name = "form_template.html"
