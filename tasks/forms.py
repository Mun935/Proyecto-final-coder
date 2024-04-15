from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'avatar']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
