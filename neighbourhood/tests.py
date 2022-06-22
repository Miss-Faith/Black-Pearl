from django.test import TestCase
from .models import *

# Create your tests here.
class TestProfile(TestCase):
    '''
    Test case for the Profile class
    '''
    def setUp(self):
        '''
        Method that creates an instance of User class
        '''
        self.user = User(id=1, username='faith', email='faith@gmail.com', password='pass')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='faith')
        self.neighbourhood = NeighbourHood.objects.create(id=1, name='kijiji', location='here', occupants=1, user=self.user, health='0722yy', police='0722gg')
        self.post = Post.objects.create(id=1, title='test post', post='post post post', date='now', user=self.user, neighbourhood=self.neighbourhood)

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_post(self):
        self.post.save()
        post = Post.objects.all()
        self.assertTrue(len(post) > 0)

    def test_search_post(self):
        self.post.save()
        post = Post.get_post_by_neighbourhood(1)
        self.assertTrue(len(post) > 0)



class TestNeighbourhood(TestCase):
    '''
    Test case for the Neighbourhood class
    '''

    def setUp(self):
        '''
        Method that creates an instance of Profile class
        '''
        self.user = User.objects.create(id=1, username='faith')
        self.neighbourhood = NeighbourHood.objects.create(id=1, name='kijiji', location='here', occupants=1, user=self.user, health='0722yy', police='0722gg')

    def test_instance(self):
        '''
        Test case to check if self.neighbourhood in an instance of Neighbourhood class
        '''
        self.assertTrue(isinstance(self.neighbourhood, NeighbourHood))

    def test_save_neighbourhood(self):
        self.neighbourhood.save()
        neighbourhood = NeighbourHood.objects.all()
        self.assertTrue(len(neighbourhood) > 0)

    def test_update_neighbourhood(self):
        self.neighbourhood.save()
        self.neighbourhood.update_neighbourhood(self.neighbourhood.name, 'kijiji')
        updated_name = NeighbourHood.objects.filter(name="town")
        self.assertFalse(len(updated_name) > 0)

    def test_delete_neighbourhood(self):
        self.neighbourhood.delete()
        neighbourhood = NeighbourHood.objects.all()
        self.assertTrue(len(neighbourhood) == 0)
