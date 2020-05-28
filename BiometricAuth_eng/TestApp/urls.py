from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.IndexPage.as_view(), name='index'),
    path('accounts/', include('BiometricAuth.urls')),
    path('personal-account/', views.PersonalAccount.as_view(), name='personal-account')
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )