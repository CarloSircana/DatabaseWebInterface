from django import forms
from django.core.exceptions import ValidationError
import django.core.validators as val
from django.utils.translation import gettext_lazy as _
import re
from .helper import Helper


class InputForm(forms.Form):

    def galois_validation(value):
        helper = Helper()
        v = helper.galois_check(value)

        if v == True:
            pass
        else:
            raise ValidationError(
                _('enter only two positive whole numbers seperated by t, T or ,'), code = 'invalid',
                params={'value': value},) 
    
    def sig_validation(value):
        input_list = value.split(',')
        if len(input_list) != 2:
            raise ValidationError(
            _('enter two numbers seperated by comma'),
            params={'value': value})

    def degree_disc_validation(value):
        if ',' in value:
            input_list = value.split(',')
            if len(input_list) != 2:
                raise ValidationError(
                _('enter maximum two numbers seperated by comma'), code = 'invalid',
                params={'value': value})
            else:
                try:
                    if int(input_list[0]) > int(input_list[1]):
                        raise ValidationError(
                        _('enter numbers in ascending order'), code = 'invalid',
                        params={'value': value})
                except ValueError:
                    pass
    
    def class_group_validation(value):
        helper = Helper()
        v = helper.class_group_check(value)

        if v == True:
            pass
        else:
            raise ValidationError(
                _('enter positive whole number(s), for structure: the first number must be divisible by all others and start and end with braces'), code = 'invalid',
                params={'value': value},)
       
    
    degree = forms.CharField(help_text='e.g. 2', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter positive whole number(s)', code='invalid', allow_negative=False), degree_disc_validation])
    
    discriminant = forms.CharField(help_text='e.g. -1000,-1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter whole number(s)', code='invalid', allow_negative=True), degree_disc_validation])
    
    cm = forms.CharField(help_text='e.g. t or f', required=False, 
        validators=[val.RegexValidator(regex=re.compile('t|f|T|F'), message='enter t or f', code = 'invalid')])
    
    signature = forms.CharField(help_text='e.g. 1,1 ', required=False, 
        validators=[val.int_list_validator(sep=',', message='enter positive whole numbers', code='invalid', allow_negative=False), sig_validation])
    
    galois_group = forms.CharField(help_text=' e.g. 2T1 or 2,1', required=False, 
        validators= [galois_validation] )
        # val.RegexValidator(regex=re.compile('[,|t|T]'), message='enter two numbers seperated by comma, T or t', code = 'invalid'), 
        # [val.int_list_validator(sep=',' or 't' or 'T', message='enter positive whole numbers', code='invalid', allow_negative=False),
    class_group = forms.CharField(help_text='e.g. number = 1 or structure = {2,4 ...}, for structure: open and close with braces ({})', required=False, 
        validators=[class_group_validation])

    
    
    def clean(self):
        self.cleaned_data = super().clean()
        degree = self.cleaned_data.get("degree")
        signature = self.cleaned_data.get("signature")

        if degree and signature:
            # Only do something if both fields are valid so far.
            sig = signature.split(',')
            # print(int(sig[0]) + 2*int(sig[1]))
            # print(degree)
            if int(degree) != int(sig[0]) + 2*int(sig[1]):
                raise forms.ValidationError(
                    "degree and signature do not match (degree = r+2s)"
                )