from django.db import models
from apps.users.models import User
from apps.organizations.models import Organization
from apps.core.models import BaseModel


class StatusChoices(models.TextChoices):
    PLANNING = ('planning', 'در حال برنامه ریزی')
    ACTIVE = ('active', 'در دست انجام')
    ON_HOLD = ('on_hold', 'متوقف')
    COMPLETED = ('completed', 'انجام شده')
    ARCHIVED = ('archived', 'آرشیو شده')

class Project(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_owner')
    members = models.ManyToManyField(User, related_name='projectsmembers', blank=True)
    status = models.CharField(max_length=200, choices=StatusChoices.choices,
                              default=StatusChoices.PLANNING)
    deadline = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه'

    def __str__(self):
        return self.name








