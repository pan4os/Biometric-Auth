from django import forms
from . import models
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth import authenticate
# from abc import ABC
# class UserBiometry(forms.ModelForm):
#     class Meta:
#     model = buildingImages
#     fields = ('buildingImage',)
#     labels = {
#         'buildingImage': ('buildingImage',),
#     }
#     exclude = ()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Нет такого пользователя')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
            if not user.is_active:
                raise forms.ValidationError('Пользователь не активен')
        return super().clean(*args, **kwargs)


# class ITwoFactorAuthFormMixin(ABC, forms.Form):
#     auth_type = None

class IrisAuth(forms.Form):
    auth_type = forms.CharField(widget=forms.HiddenInput(), initial='iris')
    iris_image = forms.ImageField()
    # pass
    # def clean(sel, *args, **kwargs):


class IrisImagesForm(forms.ModelForm):
    class Meta:
        model = models.IrisImages
        fields = '__all__'


IrisImagesFormset = inlineformset_factory(
    models.UserBiometry,
    models.IrisImages, 
    fields=('iris_image',), 
    extra=1,
    can_delete=True
    )
                                           