from django.urls import path

from .views import homeView, transferView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', homeView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

