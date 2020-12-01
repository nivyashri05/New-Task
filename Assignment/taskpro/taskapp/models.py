from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**extra_fields):
        user = self.create_user(email,password=password,**extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email= models.EmailField(verbose_name='email address',max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=False)
    phone = models.CharField(max_length=10, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
        
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="users")
    otp =  models.IntegerField(default=1, blank=True, null=True)


