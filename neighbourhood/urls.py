from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='index.html'),name = 'index'),
    path('signup/', signup, name='signup'),
]