from dataclasses import fields
from django.db import models
from django import forms
from toy.models import *

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    class Meta:
        model = Person
        fields = ['name', 'birth_date']
    
class EyeForm(forms.ModelForm):
    #colors = forms.MultipleChoiceField(widget=forms.RadioSelect, required=False, choices=EyeColor.EYE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    class Meta:
        model = EyeColor
        fields = ["color_name"]