from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import re


# Form for user registration
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=200,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Username'}),
                               required=False)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=False)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Same Password'}),
        required=False)
    first_name = forms.CharField(max_length=200,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}),
                                required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise forms.ValidationError("This field is required")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1 == "":
            raise forms.ValidationError("This field is required")
        if len(password1) < 8:
            raise forms.ValidationError(
                "This password is too short. It must contain at least 8 characters")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password2 == "":
            raise forms.ValidationError("This field is required")
        if password1 != password2:
            print(password1, password2)
            raise forms.ValidationError("The two password fields didn't match")
        return password2

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                  'password2')


# Form for user login
class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == "":
            raise forms.ValidationError("Username or password is invalid")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username or password is invalid")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password == "":
            raise forms.ValidationError("This field is required")
        return password

    def login(self, request):
        if not self.is_valid():
            return None

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return user
        else:
            self.add_error('password', "Username or password is invalid")
            return None


# Form for updating user profile
class ProfileForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=False,
        label="New password",
        help_text="Leave empty if you do not want to change the password."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        required=False,
        label="Confirm new password"
    )
    first_name = forms.CharField(max_length=200,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}),
                                required=False)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError(
                "This password is too short. It must contain at least 8 characters")
        if password1 == "":
            pass
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            print(password1, password2)
            raise forms.ValidationError("The two password fields didn't match")
        elif password1 == "" and password2 == "":
            pass
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email == "":
            pass
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Enter a valid email address")
        return email

    def save(self, ref):
        user = None
        if self.is_valid():
            user = ref
            user.email = self.cleaned_data.get('email')
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            password1 = self.cleaned_data.get('password1')
            if password1 != "":
                print("password changed")
                user.set_password(password1)
            else:
                pass
            user.save()
        return user
