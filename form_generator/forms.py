from django import forms


class FormCreate(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'placeholder': 'Example: Tenant application form 1'}))


class CustomForm(forms.Form):
    pass
