from django import forms

class dataForm(forms.Form):
    link = forms.CharField(max_length = 1000, widget = forms.TextInput(attrs={'placeholder': 'Enter Link'}))
    inputtext = forms.CharField(max_length = 1000, widget = forms.TextInput(attrs={'placeholder': 'Enter Text'}))
    option = forms.ChoiceField(choices = [('Extractive', 'Extractive'), ('Abstractive', 'Abstractive')])