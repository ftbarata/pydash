from django.forms import models
from .models import UserProfile
from django import forms


class ProfileForm(models.ModelForm):

    class Meta:

        model = UserProfile
        fields = '__all__'
        widgets={
            'username': forms.TextInput(attrs={'readonly':'readonly'}),
            'lotacao': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly', 'size': '50'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(),
            'notification_groups': forms.CheckboxSelectMultiple(),
        }


class ProfileFormReadOnly(models.ModelForm):

    class Meta:

        model = UserProfile
        fields = ['notification_groups']
        widgets={
            'notification_groups': forms.Textarea()
        }
