from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import UserLoginForm, IrisAuth,FaceAuth, FingerPrintAuth

from .authenticate import (
    IrisAuthBackend,
    FaceAuthBackend,
    FingerPrintAuthBackend
)
from .models import (
    UserBiometry,
    IrisImages,
    FaceImages,
    FingerPrintImages
)
from .utils import base64_file

class SignUp(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "BiometricAuth/signup.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def custom_logout(request):
    print('Loggin out {}'.format(request.user))
    logout(request)
    return HttpResponseRedirect('/')


class LogIn(View):
    html_template = 'BiometricAuth/login.html'

    def get(self, request):
        form = UserLoginForm()
        context = {
            'form' : form
        }
        return render(request, self.html_template, context=context)

    def post(self, request):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user_pk = User.objects.get(username=username).pk
            except User.DoesNotExist:
                raise Http404()
            user_biometry = None
            try:
                user_biometry = UserBiometry.objects.get(user__pk=user_pk)
            except UserBiometry.DoesNotExist:
                raise Http404()
            if user_biometry.iris_photo_counter or user_biometry.face_photo_counter or user_biometry.fingerprint_photo_counter:
                request.session['username'] = username
                request.session['password'] = password
                request.session['user_pk'] = user_pk
                return redirect('two-factor-auth')
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error(None, "УПС! Совпадений не найдено...")
        else:
            context = {
                'form' : form
            }
            return render(request, self.html_template, context=context)

class TwoFactorAuth(View):
    next_page = '/'

    def get(self, request):
        auth_forms = {
            'iris': IrisAuth(),
            'face': FaceAuth(),
            'fingerprint': FingerPrintAuth()
        }
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        user_pk = request.session.get('user_pk', None)
        if not username or not password or not user_pk:
            raise Http404()
        try:
            user_biometry = UserBiometry.objects.get(user__pk=user_pk)
        except UserBiometry.DoesNotExist:
            raise Http404()
        context = {
            'user_biometry':user_biometry,
            'auth_forms':auth_forms,
        }
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)


    def post(self, request):
        auth_forms = {
            'iris': IrisAuth(),
            'face': FaceAuth(),
            'fingerprint': FingerPrintAuth(),
        }
        form_type = request.POST.get('auth_type').strip()
        print('Form type={}'.format(form_type))
        username = request.session.get('username', None)
        password = request.session.get('password', None)
        user_pk = request.session.get('user_pk', None)
        if not username or not password or not user_pk:
            raise Http404()
        try:
            user_biometry = UserBiometry.objects.get(user__pk=user_pk)
        except UserBiometry.DoesNotExist:
            raise Http404()

        if form_type == 'iris':
            form = IrisAuth(request.POST or None, request.FILES or None)
            if form.is_valid():
                iris_image = form.cleaned_data.get('iris_image')
                iris_auth = IrisAuthBackend()
                user = iris_auth.authenticate(username=username, password=password, uploaded_iris=iris_image)
                if user is not None:
                    login(request, user)
                    if self.next_page:
                        return redirect(self.next_page)
                    return redirect('/')
                else:
                    form.add_error(None, "УПС! Совпадений не найдено...")
                    auth_forms['iris'] = form
            else:
                auth_forms['iris'] = form

        elif form_type == 'fingerprint':
            form = FingerPrintAuth(request.POST or None, request.FILES or None)
            if form.is_valid():
                fingerprint_image = form.cleaned_data.get('fingerprint_image')
                fingerprint_auth = FingerPrintAuthBackend()
                user = fingerprint_auth.authenticate(username=username, password=password, uploaded_fingerprint=fingerprint_image)
                if user is not None:
                    login(request, user)
                    if self.next_page:
                        return redirect(self.next_page)
                    return redirect('/')
                else:
                    form.add_error(None, "УПС! Совпадений не найдено...")
                    auth_forms['fingerprint'] = form
            else:
                auth_forms['fingerprint'] = form


        elif form_type == 'face':
            form = FaceAuth(request.POST or None, request.FILES or None)
            if form.is_valid():
                face_image = form.cleaned_data.get('face_image')
                face_image_uri = form.cleaned_data.get('face_webcam_image_uri')
                # print(type(face_image))
                # print(face_image_uri)
                if face_image_uri:
                    face_image = base64_file(face_image_uri, 'temp')
                face_auth = FaceAuthBackend()
                user = face_auth.authenticate(username=username, password=password, uploaded_face=face_image)
                if user is not None:
                    login(request, user)
                    if self.next_page:
                        return redirect(self.next_page)
                    return redirect('/')
                else:
                    form.add_error(None, "УПС! Совпадений не найдено...")
                    auth_forms['face'] = form
            else:
                auth_forms['face'] = form

        context = {
            'user_biometry': user_biometry,
            'auth_forms': auth_forms,
        }
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)
