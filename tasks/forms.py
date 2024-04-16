from django import forms
from .models import Task, Profile
from django.contrib.auth.forms import UserChangeForm

class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['username', 'email', 'avatar']
