from django import forms
from django.core.exceptions import ValidationError
import django.core.validators as val
from django.utils.translation import gettext_lazy as _
import re


class InputForm(forms.Form):
    degree = forms.IntegerField(help_text='e.g. 2', required=False, validators=[val.MinValueValidator(1,message='enter a positive integer')], localize=True)
    
    discriminant = forms.CharField(help_text='e.g. -1000,-1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=True), 
        val.MaxLengthValidator(2,message='enter maximum 2 numbers')])
    
    cm = forms.CharField(help_text='e.g. t or f', required=False, 
        validators=[val.RegexValidator(regex=re.compile('t|f|T|F'), message='enter t or f')])
    
    signature = forms.CharField(help_text='e.g. 1,1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter positive whole numbers', code='invalid', allow_negative=False), 
        val.MinLengthValidator(2,message='enter 2 numbers'), val.MaxLengthValidator(2,message='enter 2 numbers')])
    
    galois_group = forms.CharField(help_text=' e.g. 2T1 or 2,1', required=False, 
        validators=[val.int_list_validator(sep=',' or 'T' or 't', message='enter whole numbers', code='invalid', allow_negative=False), 
        val.MinLengthValidator(2,message='enter 2 numbers'), val.MaxLengthValidator(2,message='enter 2 numbers')] )
   
    class_group = forms.CharField(help_text='id = 1 or structure = 2,4 ...', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=False)])

    