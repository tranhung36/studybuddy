from django import forms
from django import forms
from django.forms import fields, widgets
from django import forms
from .models import Room
from django.contrib.auth.models import User


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        widgets = {
            'name': widgets.TextInput(attrs={'placeholder': "E.g. Mastering Python + Django"}),
            'description': widgets.Textarea(attrs={'placeholder': "Write about your study group..."})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
