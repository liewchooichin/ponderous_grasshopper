# README

## To use Azure Email Backend

Note: Partly successful. Problem with *reset_link--uid and token*.

This is how to specify the **EMAIL_BACKEND** in the **settings.py**.
```
EMAIL_BACKEND = 'django_azure_communication_email.EmailBackend'
AZURE_KEY_CREDENTIAL = config("AZURE_COMM_KEY", "")
AZURE_COMMUNICATION_ENDPOINT = config("AZURE_COMM_ENDPOINT", "")
```

Add this to the **urls.py**.
```
path(
    route="accounts/password_reset/", 
    view=home_views.my_password_reset_view,
    name="my_password_reset_view"
    ),
```

Finally, add the **my_password_reset_view** to **views.py**.

However, I still have problem getting the **uid** and **token** for the `reset_link`.

```
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

```

## To create new app in this repo

Go to the outer **hello** directory, where the **manage.py** is located. Start a new app in this directory. The outer **hello** is the **project directory**.

```
cd hello\
python manage.py startapp home
python manage.py check
```

## Location for templates

Location for **templates** is usually in the same level as the **manage.py** directory. Whether to place the **templates** in the **project** or the **app** directory is a matter of choice. Placing all `html` in the project directory is the approach in *Django in Action*.



# Useful info for deployment to Azure web apps

## Add a startup command

This is following the suggestion in [Example startup commands](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python#example-startup-commands)

```
# <module-path> is the relative path to the folder that contains the module
# that contains wsgi.py; <module> is the name of the folder containing wsgi.py.
gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 --chdir <module_path> <module>.wsgi
gunicorn --bind=0.0.0.0 --timeout 600 --workers=4 --chdir hello hello.wsgi
```

![startup command](notes/startup_command.png)

## ALLOWED_HOSTS warning

Ignore warning like that shown below. Actually when this warning is showing, it means the app deployment is running successfully.

```
2024-06-28T09:57:44.8286114Z django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: '169.254.129.7:8000'. You may need to add '169.254.129.7' to ALLOWED_HOSTS.
```

In `DEBUG` mode, set   `ALLOWED_HOSTS=localhost'.

## Key vault usage

In the environment, specify the key like this:

`@Microsoft.KeyVault(VaultName:<my_vault_name>;SecretName:<my_secret_name_in_the_vault>)

## Environment variables

```
ALLOWED_HOSTS=<my_app_name>.azurewebsites.net
DEBUG=true
DISABLE_COLLECTSTATIC=false
PRE_BUILD_COMMAND=echo Pre-build command
POST_BUILD_COMMAND=echo Post-build command
SCM_DO_BUILD_DURING_DEPLOYMENT=true
SECRET_KEY=@Microsoft.KeyVault(VaultName:<my_vault_name>;SecretName:<my_secret_name_in_the_vault>)
SQL_DRIVER=ODBC Driver 18 for SQL Server
SQL_SERVER=<my_sql_server_name>.database.windows.net
SQL_NAME=<my_sql_database_name>
SQL_USER=<sql_username>
SQL_PASSWORD=<sql_password>
WEBSITE_HTTPLOGGING_RETENTION_DAYS=3
```

## To use this template

Change the name `hello` to the name of a new app.

Reference repository for future:
- `green-engine`: The Django template from Codespaces.
- `purple-potato`: Creating REST API with Python, Django and Azure SQL. The sample from Microsoft Learn.
- `singing_cricket`: This repository combines the features from both the Django template and the REST API examples.

## Notes on create a new repository

```
echo "# singing_cricket" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/liewchooichin/singing_cricket.git
git push -u origin main
```

