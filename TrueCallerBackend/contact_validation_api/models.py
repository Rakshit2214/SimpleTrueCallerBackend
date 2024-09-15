from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class AuthDetailStore(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']
    is_anonymous = False
    is_authenticated = True
    is_active = True

    def __str__(self):
            return self.username

    def get_username(self):
            return self.username

    def has_perm(self, perm, obj=None):
            return True

    def has_module_perms(self, app_label):
            return True


class RegisteredAppUser(models.Model):
    name = models.CharField(max_length=255)
    username = models.ForeignKey(AuthDetailStore, on_delete=models.CASCADE)
    registeredUserNumber = models.CharField(max_length=15, unique=True)
    userEmailId = models.EmailField(null=True, blank=True, unique=True)


class ContactStoreBO(models.Model):
    registeredContactOwner = models.ForeignKey(RegisteredAppUser,
                                                   related_name='contacts', on_delete=models.CASCADE)
    ContactName = models.CharField(max_length=255)
    ContactNumber = models.CharField(max_length=15)
    ContactEmailId = models.EmailField(null=True, blank=True)
    ContactSpamValue = models.FloatField(default=0.0)
    ContactIsSpam = models.BooleanField(default=False)
