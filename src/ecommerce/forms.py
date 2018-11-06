from django import forms
from django.contrib.auth import get_user_model

user=get_user_model()     

class ContactForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control", 
                "id":"form_full_name"
                }
            )
            )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class":"form-control", 
                "id":"form_full_name"
                }

            )
        )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control", 
                "id":"form_full_name"
                }
            )
        )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 

class RegisterForm(forms.Form):
    username = forms.CharField()
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput) 
    passwordc = forms.CharField(label='Confirm Password',widget=forms.PasswordInput) 

    def clean_username(self):
        username=self.cleaned_data.get("username")
        qs = user.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username 

    def clean_email(self):
        email=self.cleaned_data.get("email")
        qs = user.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email already exists")
        return email 

    def clean(self):
        data=self.cleaned_data
        password=self.cleaned_data.get("password")
        passwordc=self.cleaned_data.get("passwordc")
        if passwordc != password:
            raise forms.ValidationError("Passwords must Match...")
        return data

