from django import forms
from django.core.exceptions import ValidationError
import django.core.validators as val

class InputForm(forms.Form):
    degree = forms.IntegerField(help_text='degree = 2,3..', required=False, validators=[val.MinValueValidator(1,message='please enter a positive integer')], localize=True)
    discriminant = forms.CharField(help_text='discriminant = -1000,-1  ...', required=False)
    cm = forms.CharField(help_text='cm = t or f', required=False)
    signature = forms.CharField(help_text='signature = 1,1 ...', required=False)
    galois_group = forms.CharField(help_text='nTk or n,k', required=False)
    class_group = forms.CharField(help_text='id = n or structure = n1,n2', required=False)