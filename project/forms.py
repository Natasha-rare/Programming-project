from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    roles = (("1", "Ученик"), ("2", "Учитель"))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'reg_input',
                                                         'placeholder': " "}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'reg_input', 'placeholder': " "}))
    father = forms.CharField(widget=forms.TextInput(attrs={'class': 'reg_input', 'placeholder': " "}))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={'class': 'reg_input',
                                                                                                 'type': 'email',
                                                                                                 'placeholder': " "}))
    status = forms.ChoiceField(choices=roles, widget=forms.RadioSelect)
    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(attrs={'class': 'reg_input',
                                                                 'autocomplete': 'new-password', 'placeholder': " "}),
    )

    # подтверждение пароля
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'reg_input',
                                          'autocomplete': 'new-password', 'placeholder': " "}),
        strip=False,
    )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    class Meta:
        model = User
        fields = ('name', 'surname', 'father', 'email', 'password', 'password2')
