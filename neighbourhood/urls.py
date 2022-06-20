from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='index.html'),name = 'index'),
    path('signup/', signup, name='signup'),
    path('neighbourhoods/', hoods, name='hood'),
    path('register/', signup, name='signup'),
    path('new-hood/', create_hood, name='new-hood'),
    path('profile/<username>', profile, name='profile'),
    path('profile/<username>/edit/', edit_profile, name='edit-profile'),
    path('join_hood/<id>', join_hood, name='join-hood'),
    path('leave_hood/<id>', leave_hood, name='leave_hood'),
    path('hood/', single_hood, name='single_hood'),
    path('<hood_id>/new-post', create_post, name='post'),
    path('<hood_id>/accounts', hood_accounts, name='accounts'),
    path('search/', search_business, name='search'),
]