from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'
        db_table = 'users'


    def __str__(self):
        return self.username