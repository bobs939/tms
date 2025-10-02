from django import forms
from .models import Target

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['name', 'description', 'department', 'sub_department', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'sub_department': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
        }