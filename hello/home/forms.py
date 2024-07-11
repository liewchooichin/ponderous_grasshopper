# Password reset form

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from .azure_email import send_with_azure_email


class MyPasswordResetForm(PasswordResetForm):
    """Custom password reset form to be used with custom
        email backend.
    """
    #user_email = forms.EmailField(label="Email", max_length=100)
    
    # context – context passed to the subject_template, 
    # email_template, and html_email_template
    # subject_template_name¶:  Defaults to registration/password_reset_subject.txt
    # email_template_name: Defaults to registration/password_reset_email.html
    # DEFAULT_FROM_EMAIL¶: Default: 'webmaster@localhost'
    # html_email_template_name: Default to None

    # My variables for use with custom email backend
    from_email = "<DoNotReply@f0cf672a-d027-4901-bfea-018e517e7e1c.azurecomm.net>"
    
    #send_with_azure_email(from_email=from_email)
    #send_mail(subject="Difficult subject",
    #          message="Django is difficult",
    #          from_email=from_email,
    #          recipient_list=["liewchooichin@gmail.com"]
    #         )