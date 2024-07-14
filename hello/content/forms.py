# App content

from django import forms

from content.models import SeekingAd

# CommentForm
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
    subject = forms.CharField(max_length=100, 
                              label="Subject", 
                              initial="",
                              show_hidden_initial=True,
                              help_text="Topic or subject of your comment")
    comment = forms.CharField(
        max_length=300,
        label="Comments",
        initial="",
        help_text="Max length 300 characters",
        show_hidden_initial=True,
        widget=forms.Textarea(
            attrs = {"rows": "6", "cols": "50"}
        ),
    )
    # Use custom form template
    template_name = "form_template.html"


# ModelForm for the SeekingAd model
class SeekingAdForm(forms.ModelForm):
    """Associate SeekingAdForm with SeekingAd model"""
    class Meta:
        model = SeekingAd
        fields = ["seeking", "musician", "band", "ads"]

        # One way of writing the field attrs
        labels = {
            "seeking": "Seeking a musican or a band",
            "musician": "You are a musician",
            "band": "This is a band",
            "ads": "Put your ads here",
        }
        help_text = {
            "seeking": "Enter 'M' if you are looking for a \
                musician, 'B' if you are looking for a band",
            "musician": "Enter your name here",
            "band": "Enter name of your band here",
            "ads": "Max 300 characters",
        }

        # This is one way of writing the field attrs
        def __init__(self, *args, **kwargs):
            """Some modification to the form fields"""
            super().__init__(*args, **kwargs)
            #self.fields["seeking"].label = "I am seeking a"
            #self.fields["musician"].help_text = \
            #    "Fill in if you are a musician seeking a band to join"
            #self.fields["band"].help_text = \
            #    "Fill in if your band is seeking a musician"

    # Use a form template
    template_name = "form_template.html"

