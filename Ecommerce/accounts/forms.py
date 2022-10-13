from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password',
        'class':'form_control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password',
        'class':'form_control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs["placeholder"] = "Enter your First name"
        self.fields['last_name'].widget.attrs["placeholder"] = "Enter your Last name"
        self.fields['email'].widget.attrs["placeholder"] = "Enter Email Address"
        self.fields['phone_number'].widget.attrs["placeholder"] = "Enter Phone number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
    """ С помощью метода супер меняет действия init и меняет атрибуты полей формы """
