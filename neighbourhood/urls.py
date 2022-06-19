from django.urls import path
from .views import *

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='index.html'),name = 'index'),
    path('register/', views.signup, name='signup'),
]