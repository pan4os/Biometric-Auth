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
from .forms import UserLoginForm, IrisAuth
# from .iris_auth.prepare import prepare_image
from .authenticate import (
    IrisAuthBackend,

)
from .models import (
    UserBiometry,
    IrisImages,
    FaceImages,
    FingerPrintImages
)

class SignUp(FormView):
    form_class = UserCreationForm
    success_url = "/"

    template_name = "BiometricAuth/signup.html"

    def form_valid(self, form):
        form.save()
        # user = User.objects.get(form.cleaned_data.get('username'))
        # print(user)
        # UserBiometry(user=user)
        #     temp_user_biometry.save()
        return super().form_valid(form)

def custom_logout(request):
    print('Loggin out {}'.format(request.user))
    logout(request)
    print(request.user)
    return HttpResponseRedirect(request.GET.get('next','/'))

 

class LogIn(View):
    html_template = 'BiometricAuth/login.html'
    next_page = None
    # two_factor_choice_html_template = 'BiometricAuth/two_factor_auth.html'

    def get(self, request):
        self.next_page = request.GET.get('next')
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
            request.session['username'] = username
            request.session['password'] = password
            request.session['user_pk'] = user_pk
            # После успешной аутентификации :
            # user = authenticate(username=username, password=password)
            # login(request, user)
            # if self.next_page:
            #     return redirect(self.next_page)
            # return redirect('/')
            return redirect('two-factor-auth')
        else:
            context = {
                'form' : form
            }
            return render(request, self.html_template, context=context)

class TwoFactorAuth(View):

    next_page = '/'
    # user_biometry = None
    # username = None
    # password = None
    # user_pk = None
    auth_forms = {
        'iris': IrisAuth(),
    }

    def get(self, request):
        # next_page = request.GET.get('next')
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
            'auth_forms':self.auth_forms,
        }
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)


    def post(self, request):
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
            print(form)
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
                    form.add_error(None, "Username, password or face id didn't match.")
                    # self.auth_forms['iris'] = form
                    # print('\t',form )
            else:
                self.auth_forms['iris'] = form
                print('\t',form )
        # print('\t',self.auth_forms['iris'])
        context = {
            'user_biometry': user_biometry,
            'auth_forms': self.auth_forms,
        }
        # print(self.username)
        return render(request,'BiometricAuth/two_factor_auth.html', context=context)


