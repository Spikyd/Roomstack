from django import forms
from django.contrib.auth.models import User

from roommate.models import Message


class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    class Meta:
        model = Message
        fields = ['receiver', 'message']
