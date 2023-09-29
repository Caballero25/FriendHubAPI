from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    #Personal data
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='perfil_pictures/', blank=True, null=True)
    banner = models.ImageField(upload_to='banner_pictures/', blank=True, null=True)
    biography = models.TextField(max_length=200, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    #social data
    friends = models.ManyToManyField('self', blank=True)
    #permissions and groups
    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=('user permissions'), blank=True, related_name='user_user_permissions'
    )
    USERNAME_FIELD ='email'
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def mutual_friends (self, other_user):
        # Mutual friends list with other user
        my_friends = set(self.friends.all())
        friend_other_user = set(other_user.friends.all())
        # Number of mutual friends
        mutual_friends = my_friends.intersection(friend_other_user)
        # Create a list of mutual friends
        mutual_friends = list(mutual_friends)

        return len(mutual_friends), mutual_friends
    
#Auth Token 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

