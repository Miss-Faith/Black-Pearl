from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('',index,name='index'),
    path('account/', include('django.contrib.auth.urls')),
    path('profile/<profile_id>',profile,name = 'profile'),
    path('updateProfile',updateProfile,name = 'updateProfile'),
    path('updateProfile/<user_id>',updateProfile2,name = 'updateProfile2'),
    path('new/hood/',create_neighbourhood, name='newHood'),
    path('all/hoods/',neighbourhoods, name='allHoods'),
    path('neighborhood/<neighbour_id>',neighbourhood_details, name='pickHood'),
    path('post/', new_post, name='post'),
    path('search/', search_results, name='search'),
    path('occupants/<hood_id>', hood_occupants, name='occupants'),
]