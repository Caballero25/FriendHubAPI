from django.db import models
from django.contrib.auth.models import BaseUserManager
class UserManager(BaseUserManager, models.Manager):
    
    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(email, first_name, last_name, password, False, False, **extra_fields)


    def _create_super_user(self, email, password, **extra_fields):
        user = self.model(
            email = email,
            first_name = "admin",
            last_name = "admin",
            password = password,
            is_staff = True,
            is_superuser = True,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        # Con el _ la hacemos privada esto evita que se pueda acceder de otro la do que no sea la terminal.
        return self._create_super_user(email, password, **extra_fields)