from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/',views.SignUp.as_view(), name='sign-up'),
    path('sign-in/', views.LogIn.as_view(), name='sign-in'),
    path('two-factor-auth/', views.TwoFactorAuth.as_view(), name='two-factor-auth'),
    path('logout/', views.custom_logout, name='logout'),
]