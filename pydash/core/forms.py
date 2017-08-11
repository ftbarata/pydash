from .models import Group
from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(max_length=1000, initial='Mensagem', widget=forms.Textarea(attrs={'class': 'textarea'}))
    detailed_message = forms.CharField(max_length=1000, initial='Mensagem técnica detalhada', widget=forms.Textarea(attrs={'class': 'textarea'}))
    severity = forms.CharField(max_length=20)


class GroupForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(Group.objects.all())

