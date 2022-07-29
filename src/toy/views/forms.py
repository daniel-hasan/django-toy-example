from dataclasses import fields
from django.db import models
from django import forms
from toy.models import *
from toy_example import settings

class DateInput(forms.DateInput):
    input_type = "date"

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    class Meta:
        model = Person
        fields = ['name', 'birth_date']
        widgets = {
            'birth_date': DateInput()
        }
    
class EyeForm(forms.ModelForm):
    colors = forms.MultipleChoiceField(widget=forms.RadioSelect, choices=EyeColor.EYE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    class Meta:
        model = EyeColor
        fields = ["colors"]