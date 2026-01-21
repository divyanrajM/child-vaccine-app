from django import forms
from .models import Child


class LookupForm(forms.Form):
    """Form for looking up a child by RCSH Number or Parent Number"""
    search_value = forms.CharField(
        max_length=20,
        label='RCH Number or Parent Number',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter RCH Number or Parent Number',
            'autocomplete': 'off'
        })
    )


class ChildForm(forms.ModelForm):
    """Form for registering/editing child details"""
    
    class Meta:
        model = Child
        fields = ['rch_number', 'parent_number', 'child_name', 'date_of_birth', 'sex']
        widgets = {
            'rch_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter RCH Number'
            }),
            'parent_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Parent Number'
            }),
            'child_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Child Name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'sex': forms.Select(attrs={
                'class': 'form-input'
            }),
        }
