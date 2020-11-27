from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django_summernote.models import AbstractAttachment


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20, null=False, unique=True)
    gender = models.CharField(max_length=1, null=False)


class Post(models.Model):
    title = models.CharField(max_length=50)
    first_date = models.DateField()
    last_date = models.DateField()
    location = models.CharField(max_length=255)
    route = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Attachment(AbstractAttachment):
    pass