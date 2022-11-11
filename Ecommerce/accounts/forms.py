from django import forms
from .models import Account, UserProfile

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
        """ С помощью метода супер меняет действия init и меняет атрибуты полей формы """
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs["placeholder"] = "Enter First Name"
        self.fields['last_name'].widget.attrs["placeholder"] = "Enter Last Name"
        self.fields['email'].widget.attrs["placeholder"] = "Enter Email Address"
        self.fields['phone_number'].widget.attrs["placeholder"] = "Enter Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"



    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean() # https://docs.djangoproject.com/en/4.1/ref/forms/validation/
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )
        """The clean() method on a Field subclass is responsible for running to_python(), validate(), 
        and run_validators() in the correct order and propagating their errors. If, at any time, any of the 
        methods raise ValidationError, the validation stops and that error is raised. This method returns the 
        clean data, which is then inserted into the cleaned_data dictionary of the form.
        def clean проверяет на соответствие пароля и повторного пароля при регистрации и из-за использования 
        метода clean() возвращает ошибки, но нужно не забыть в шаблоне прописать теги для возвращения ошибок пользователю:
        """


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        """ С помощью метода супер меняет действия init и меняет атрибуты полей формы """
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, error_messages= {'invalid': ("Image files only")}, widget=forms.FileInput
    ) # убирает надпись с наименованием файла модели над формой
    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        """ С помощью метода супер меняет действия init и меняет атрибуты полей формы """
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"