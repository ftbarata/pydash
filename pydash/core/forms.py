from .models import Group
from django import forms


# class MessageForm(ModelForm):
#     class Meta:
#         model = Message
#         fields = ['message', 'severity']

class MessageForm(forms.Form):
    message = forms.CharField(max_length=1000, initial='Mensagem', widget=forms.Textarea(attrs={'class': 'textarea'}))
    detailed_message = forms.CharField(max_length=1000, initial='Mensagem técnica detalhada', widget=forms.Textarea(attrs={'class': 'textarea'}))
    severity = forms.CharField(max_length=20)

# class GroupForm(ModelForm):
#
#     class Meta:
#         model = Group
#         fields = ['id', 'name']
#         groups = Group.objects.all()
#         widgets = {'name': SelectMultiple(choices=groups.values_list('id', 'name'))}


class GroupForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(Group.objects.all())
