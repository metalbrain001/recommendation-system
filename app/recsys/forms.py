"""
This module contains the form for user registration.
"""

from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(attrs={"class": "form-email"}),
        help_text="Enter your email address",
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-name"}),
        help_text="Enter your full name",
    )
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-password"})
    )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["name"].required = True
        self.fields["password"].required = True
