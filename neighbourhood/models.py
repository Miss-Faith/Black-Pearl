from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
import os
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class NeighbourHood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants=models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='neighbourhood', blank=True)
    health = PhoneNumberField(null = False, blank = False)
    police = PhoneNumberField(null = False, blank = False)
    
    def __str__(self):
        return f'{self.name} neighbourhood'

    def create_neighbourhood(self):
        self.save()

    def delete_neighbourhood(self):
        self.delete()

    def update_neighbourhood(self, name, value):
        NeighbourHood.objects.filter(name=name).update(name=value)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, null=True, related_name='profile', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Business(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='business')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def update_business(cls, name, email, description, neighbourhood):
        update = cls.objects.filter(id = id).update(name = name, location = location, description = description)

    @classmethod
    def search_business(cls, search_term):
            businesses = cls.objects.filter(name__icontains=search_term)
            return businesses

class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_post_by_neighbourhood(cls,neighbourhood_id):
        messages = cls.objects.all().filter(neighbourhood=neighbourhood_id)
        return messages
