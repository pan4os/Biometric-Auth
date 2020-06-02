from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404
from BiometricAuth.models import (
    UserBiometry, 
    IrisImages,
    FaceImages
)
from BiometricAuth.forms import (
    IrisImagesFormset, 
    IrisImagesForm,
    FaceImagesForm,
    FaceImagesFormset
)

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
        
        formsets = {
            'iris_formset':IrisImagesFormset(instance=user_biometry, prefix='iris_image'),
            'face_formset':FaceImagesFormset(instance=user_biometry, prefix='face_image'),

        }


        context = {
            'formsets' : formsets
        }
        # context = {
        #     'iris_formset' : iris_formset
        # }
        return render(request, 'TestApp/personal_account.html', context=context)

    def post(self, request):
        if not request.user.is_authenticated:
            raise Http404

        user_biometry = get_object_or_404(UserBiometry, user=request.user.id)
        formsets = {
            'iris_formset':IrisImagesFormset(instance=user_biometry, prefix='iris_image'),
            'face_formset':FaceImagesFormset(instance=user_biometry, prefix='face_image'),
            
        }
        form_type = request.POST.get('form_type').strip()
        print('Form type={}'.format(form_type))
        if form_type == 'iris':
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
                # Чтобы отобразить ошибки
                formsets['iris_formset'] = iris_formset

        elif form_type == 'finger_print':
            pass
        elif form_type == 'face':
            face_formset = FaceImagesFormset(
                request.POST or None, 
                request.FILES or None, 
                prefix='face_image',
                instance = user_biometry
                )
            if face_formset.is_valid():
                for form in face_formset:
                    # Обновляем счетчик для каждой измененной формы
                    if form.has_changed():
                        if form.cleaned_data.get('DELETE'):
                            user_biometry.change_face_photo_counter(increase = False)
                            user_biometry.save()
                        elif face_image := form.cleaned_data.get('face_image'):

                            user_biometry.change_face_photo_counter()
                            user_biometry.save()

                print('Счетчик: ', user_biometry.face_photo_counter)
                face_formset.save()
                
                return redirect('personal-account')
            else:
                # Чтобы отобразить ошибки
                formsets['face_formset'] = face_formset


        context = {
            'formsets' : formsets,

        }
        return render(request, 'TestApp/personal_account.html', context=context)
        