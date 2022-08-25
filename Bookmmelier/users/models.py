from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model
import hashlib

class UserManager(BaseUserManager):
    def create_user(self, id, name, password, email,gender, age, hash, type):
        if not id:
            raise ValueError('Users must have an id')
        if not name:
            raise ValueError('Users must have an name')
        if not email:
            raise ValueError('Users must have an email address')
        if not gender:
            raise ValueError('Users must have an email address')
        if not age:
            raise ValueError('Users must have an email address')

        user = self.model(
            id = id,
            name = name,
            email=self.normalize_email(email),
            gender = gender,
            age = age,
            hash = hash,
            type = type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, name, password, email,gender, age):

        user = self.create_user(
            id = id,
            name = name,
            email=self.normalize_email(email),
            password=password,
            gender = gender,
            age = age,
            type = 'super'
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):  
   objects = UserManager()

   id = models.CharField(primary_key=True, max_length=30,unique=True)
   name = models.CharField(max_length=10,unique=False,null=True)
   gender = models.CharField(max_length=10,unique=False,null=True)
   age = models.CharField(max_length=10,unique=False,null=True)
   email = models.EmailField(max_length=255,unique=True,null=True)
   hash = models.CharField(max_length=100,unique=False,null=True)
   type = models.CharField(max_length=30,unique=False,null=True)
   is_active = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   is_staff = models.BooleanField(default=False)

   USERNAME_FIELD = 'id'    
   REQUIRED_FIELDS = ['name','gender','age','email']

   def __str__(self):
       return self.id

