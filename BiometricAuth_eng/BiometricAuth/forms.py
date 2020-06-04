from django import forms
from . import models
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth import authenticate


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


# ---------------- Формы для алгоритмов

# ---------------- Радужка глаза:
class IrisAuth(forms.Form):
    '''
    Форма для страницы аутентификации.
    auth_type нужен для идентификации формы на странице двухфакторной аутентификации
    '''
    auth_type = forms.CharField(widget=forms.HiddenInput(), initial='iris')
    iris_image = forms.ImageField()


class IrisImagesForm(forms.ModelForm):
    '''
    Форма для страницы профиля (загрузка изображений в профиль)
    auth_type нужен для идентификации формы на странице профиля
    '''
    # auth_type = forms.CharField(widget=forms.HiddenInput(), initial='iris')
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


# ------------------- Лицо:
class FaceAuth(forms.Form):
    auth_type = forms.CharField(widget=forms.HiddenInput(), initial='face')
    face_image = forms.ImageField()

class FaceImagesForm(forms.ModelForm):
    '''
    Форма для страницы профиля (загрузка изображений в профиль)
    auth_type нужен для идентификации формы на странице профиля
    '''
    # auth_type = forms.CharField(widget=forms.HiddenInput(), initial='iris')
    class Meta:
        model = models.FaceImages
        fields = '__all__'

FaceImagesFormset = inlineformset_factory(
    models.UserBiometry,
    models.FaceImages,
    fields=('face_image',),
    extra=1,
    can_delete=True
    )


# ------------------- Отпечаток пальца:
class FingerPrintAuth(forms.Form):
    '''
    Форма для страницы аутентификации.
    auth_type нужен для идентификации формы на странице двухфакторной аутентификации
    '''
    auth_type = forms.CharField(widget=forms.HiddenInput(), initial='fingerprint')
    fingerprint_image = forms.ImageField()

class FingerPrintImagesForm(forms.ModelForm):
    '''
    Форма для страницы профиля (загрузка изображений в профиль)
    auth_type нужен для идентификации формы на странице профиля
    '''
    # auth_type = forms.CharField(widget=forms.HiddenInput(), initial='iris')
    class Meta:
        model = models.FingerPrintImages
        fields = '__all__'

FingerPrintImagesFormset = inlineformset_factory(
    models.UserBiometry,
    models.FingerPrintImages,
    fields=('fingerprint_image',),
    extra=1,
    can_delete=True
    )
