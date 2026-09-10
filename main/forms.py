from django import forms

class UserForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class AccountForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    name = forms.CharField(label="Name", max_length=20,
        min_length=2,widget=forms.TextInput
    )