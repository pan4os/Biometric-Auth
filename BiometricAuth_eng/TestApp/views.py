from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from BiometricAuth.models import UserBiometry, IrisImages
from BiometricAuth.forms import IrisImagesFormset, IrisImagesForm
from django.http import Http404

class IndexPage(View):
    def get(self, request):
        context = {

        }
        return render(request, 'TestApp/index.html', context=context)

class PersonalAccount(View):
    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404

        user_biometry = UserBiometry.objects.get(user=request.user.id)
       
        # # Находим обьект пользовательских биометрических данных.
        # # Если его нет - создаем.
        # user_biometry = None
        # try:
        #     user_biometry = UserBiometry.objects.get(user=request.user.id)
        # except UserBiometry.DoesNotExist:
        #     temp_user_biometry = UserBiometry(user=request.user)
        #     temp_user_biometry.save()
        #     user_biometry = temp_user_biometry
        # print(user_biometry)


        iris_formset = IrisImagesFormset(
            instance=user_biometry,
            prefix='iris_image'
            )
        context = {
            'iris_formset' : iris_formset
        }
        return render(request, 'TestApp/personal_account.html', context=context)

    def post(self, request):
        if not request.user.is_authenticated:
            raise Http404

        user_biometry = get_object_or_404(UserBiometry, user=request.user.id)
        iris_formset = IrisImagesFormset(
            request.POST or None, 
            request.FILES or None, 
            prefix='iris_image',
            instance = user_biometry
            )

        if iris_formset.is_valid():

            for form in iris_formset:
                # Обновляем счетчик для каждой измененной формы
                if form.has_changed():
                    if form.cleaned_data.get('DELETE'):
                        user_biometry.change_iris_photo_counter(increase = False)
                        user_biometry.save()
                    elif iris_image := form.cleaned_data.get('iris_image'):

                        user_biometry.change_iris_photo_counter()
                        user_biometry.save()

            print('Счетчик: ', user_biometry.iris_photo_counter)
            iris_formset.save()
            
            return redirect('personal-account')
        else:
            context = {
                'iris_formset' : iris_formset
            }
            return render(request, 'TestApp/personal_account.html', context=context)
        


        