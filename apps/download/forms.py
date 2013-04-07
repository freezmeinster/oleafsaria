from django import forms
from django.forms.widgets import CheckboxSelectMultiple

class FormDownload(forms.Form):
    
    url = forms.URLField()
    split = forms.IntegerField(widget=forms.Select(choices=[(i, i) for i in range(5,25,5)]))
