from django import forms
from django.contrib.auth.models import User

from takeaway.models import UserProfile


class UserForm(forms.ModelForm):
    # overwrite password
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'address',)
