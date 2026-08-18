from django.db import models
from apps.core.models import BaseModel
from apps.users.models import User
from apps.projects.models import Project

# Create your models here.
class Task(BaseModel):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    reporter = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='tasks_reporter')
    priority = models.IntegerField(default=0, choices=PRIORITY_CHOICES)
    is_done = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    tags = models.JSONField(default=list, blank=True)
    class Meta:
        verbose_name = 'تسک'
        verbose_name_plural = 'تسک'

    def __str__(self):
        return self.title