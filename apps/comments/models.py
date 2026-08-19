from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.tasks.models import Task
# Create your models here.

class Comment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت'

    def __str__(self):
        return f'{self.body[:100]} ...'

