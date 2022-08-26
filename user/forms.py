from django import forms
# from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        max_length=20
        )
    last_name = forms.CharField(
        max_length=20
        )
    email = forms.EmailField(
        max_length=50
        )
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = forms.ChoiceField(
        choices = GENDER
        )
    password = forms.CharField(
        widget=forms.PasswordInput()
        )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not User.objects.filter(username = email).count() == 0:
            raise forms.ValidationError("User name / email already registered")

        return email

    def clean(self):
        super().clean()

        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):  
            raise forms.ValidationError("Password didn't matched")

        for i in self.cleaned_data.items():
            print(i)
            if i[1] == "" or not i[1] :
                raise forms.ValidationError(
                    "Required Fields need to be filled: {}"
                    .format(i[0].replace("_", " "))
                    )


class LoginForm(forms.Form):
    user_name = forms.CharField()
    password = forms.CharField(
        widget = forms.PasswordInput()
    )

    def clean(self):
        super().clean()

        user = authenticate(
            username = self.cleaned_data.get("user_name"),
            password = self.cleaned_data.get("password")
        )

        if user == None:
            raise forms.ValidationError("Invalid Credentials")


        

