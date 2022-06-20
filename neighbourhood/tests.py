from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

# Create your tests here.


class ProfileTestClass(TestCase):
    '''
    Test case for the Profile class
    '''

    def setUp(self):
        '''
        Method that creates an instance of Profile class
        '''
        # Create instance of Profile class
        self.new_profile = Profile(bio="Friendly Neighbour")

    def test_instance(self):
        '''
        Test case to check if self.new_profile in an instance of Profile class
        '''
        self.assertTrue(isinstance(self.new_profile, Profile))


    def test_get_other_profiles(self):
        '''
        Test case to check if all profiles are gotten from the database
        '''
        self.name = User(username="Faith")
        self.name.save()


        self.test_profile = Profile(user=self.name, bio="Another Profile")
        gotten_profiles = Profile.get_other_profiles(self.name.id)
        profiles = Profile.objects.all()


class Neighbourhood(TestCase):
    '''
    Test case for the Neighbourhood class
    '''

    def setUp(self):
        '''
        Method that creates an instance of Profile class
        '''
        # Create a Image instance
        self.name = Neighbourhood(name='kijiji')

    def test_instance(self):
        '''
        Test case to check if self.new_Image in an instance of Image class
        '''
        self.assertTrue(isinstance(self.new_Image, Image))

class Post(TestCase):
    '''
    Test case for the Post class
    '''

    def setUp(self):
        '''
        Method that creates an instance of Post class
        '''
        # Create a Post instance
        self.title = Post(title='hey')

    def test_instance(self):
        '''
        Test case to check if self.title in an instance of Post class
        '''
        self.assertTrue(isinstance(self.title, Post.title))
