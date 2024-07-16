# My Notes


## Displaying image

Image can be displayed by specifying the **MEDIA_URL**:

When used in a **form**: `"/media/{{form.picture.value}}/"`
```
<img 
    class="img-fluid"
    src="/media/{{form.picture.value}}/"
    alt="picture of your venue"
    width="200" height="200"
>
```

When used in a **queryset**: `item.picture.url`

```
<img 
    src="{{ item.picture.url }}"
    alt="{{ item.name }}"
    width="200" height="200"
>
```

## File or image file upload

16 Jul

The form must be **`multipart/form-data`**.

```
<form enctype="multipart/form-data" method="POST">
```

## Using Developer Tools

14 Jul

Debugging the mysterious reason the `form.my_field.value` only shows the 
first word. Using the Developer Tools to look at the html generated.

`{% %}` or `{{ }}` need to be used with &quot;&quot;

```
<input 
    type="text" 
    class="form-control"
    name="{{ form.name.name }}"
    id="{{ form.name.id_for_label }}" 
    value="{{ form.name.value }}"
/>

```

Remember in **textarea**, the {{value}} is placed outside of the `<textarea>`.
```
<textarea 
    class="form-control"
    name="{{ form.description.name }}"
    id="{{ form.description.id_for_label }}"
    rows="5", cols="80">{{ form.description.value }}
</textarea>
```

## Toggle password show/hide

14 Jul

With the help of [an article from StackOverflow](https://stackoverflow.com/questions/25017403/django-show-password-checkbox), 
I manage to get the password to show/hide.

The `document.querySelector("#id_password")` is the Django password id field.

```
    <!--In the /templates/registration/login.html, add a checkbox.-->

    <input type="checkbox" id="toggle_password" 
    name="toggle_password">
    <label for="toggle_password">Show password</label>
```

```
/* 
In the /static/main.js

Useful reference:
https://stackoverflow.com/questions/25017403/django-show-password-checkbox
Important info: 
    - Django password id field: document.querySelector("#id_password")
*/

pwd_box = document.querySelector("#toggle_password")
pwd_field = document.querySelector("#id_password")

pwd_box.addEventListener("click", listener=toggle_password)

function toggle_password()
{
    console.log("Toggle pasword");
    if(pwd_box.checked)
        pwd_field.type='text';
    else
        pwd_field.type='password';
}

```


## Get the current `request.user`

14 Jul, Sun

To make a filter list according to the current login user:

```
# Get the user id of the current request.user
current_user = User.objects.get(username=request.user)
print(f"\t{request.user=} {current_user.id} {current_user.username}")
# No need to put "" around the content of the filter.
data = {
    'ad': MyModel.objects.filter(an_attr_in_MyModel=current_user.id)
}

```


## Using form template

13 Jul, Sat

Following the tutorial to create a comment form with template.

### Location of form template

When trying to use form template, I encountered the problem of the location of the template. The error encountered was **TemplateNotFound**. I tried many different locations.

The first location was `\templates\` where I have been putting the various html files. However this did not work for the form template. Finally the location that work is `\content\templates\form_template.html`. If I put the `form_template.html` in `\content\templates\content\form_template.html`, it would not work.

### Placement of button

The `<form>`, `{% csrf_token %}` and `<button>` should be put in the parent form html. The form template should contains just the from styling.


## To use Azure Email Backend

Install the package [django-azure-communication-email](https://pypi.org/project/django-azure-communication-email/)


This is how to specify the **EMAIL_BACKEND** in the **settings.py**.
```
EMAIL_BACKEND = 'django_azure_communication_email.EmailBackend'
AZURE_KEY_CREDENTIAL = config("AZURE_COMM_KEY", "")
AZURE_COMMUNICATION_ENDPOINT = config("AZURE_COMM_ENDPOINT", "")
DEFAULT_FROM_EMAIL="<Your-email-like-DoNotReply@example.com>"
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

