from django.db import models

# Create your models here.
class NeighbourHood(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    occupants = models.IntegerField(default=0, null=True, blank=True)
    admin = models.ForeignKey("Admin", on_delete=models.CASCADE, related_name='admin')
    
    def __str__(self):
        return f'{self.name} name'

    def create_neighborhood(self):
        self.save()

    def delete_neighborhood(self):
        self.delete()

    @classmethod
    def find_neighborhood(cls, id):
        return cls.objects.filter(id=id)

    @classmethod
    def update_neighbourhood(cls, name, location):
        update = cls.objects.filter(id = id).update(name = name, location = location)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.SET_NULL, null=True, related_name='neighbourhood', blank=True)

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
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='neighbourhood')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return f'{self.name} name'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()

    @classmethod
    def update_business(cls, name, email, description, neighbourhood):
        update = cls.objects.filter(id = id).update(name = name, location = location, description = description)

    @classmethod
    def find_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()


class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user')
    neighbourhood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE, related_name='neighbourhood')