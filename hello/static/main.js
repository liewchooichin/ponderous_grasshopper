/* To check if the static javascript is loaded */
console.log("Hello Bootstrap and Django.");

/* 
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


