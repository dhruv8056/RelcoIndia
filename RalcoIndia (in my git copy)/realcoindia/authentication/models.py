from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, password2=None):
        if not mobile_number:
            raise ValueError('Users must have an email address')
        user = self.model(
            mobile_number=self.normalize_email(mobile_number),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mobile_number, password=None,password2=None):
        user = self.create_user(
            mobile_number=mobile_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
    )
    FCM = models.CharField(max_length=255, null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    mobile_number = models.CharField(max_length=255,unique=True,null=True)
    otp = models.IntegerField(null=True,blank=True,default=9999)
    objects = UserManager()

    USERNAME_FIELD = 'mobile_number'

    def __str__(self):  
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin