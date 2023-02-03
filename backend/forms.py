from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class UploadJsonForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = JsonFile
        fields = ('file', )


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
