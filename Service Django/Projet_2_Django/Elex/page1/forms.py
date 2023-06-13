from django import forms

class consol(forms.Form):
    command = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True,'class':'ConsolTextInput'}))