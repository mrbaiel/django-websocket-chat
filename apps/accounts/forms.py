from cProfile import label
from logging import raiseExceptions

from django import forms
from django.core.exceptions import ValidationError

from apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='введите пароль еще раз', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number']


    def check_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password1

    def save(self, commit=True):
        """ Сохраним пароль в хэш формате"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

