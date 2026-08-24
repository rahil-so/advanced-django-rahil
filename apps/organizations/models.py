from django.db import models
from apps.users.models import User
from apps.core.models import BaseModel
# Create your models here.

class PlanChoices(models.TextChoices):
    free = ('free', 'رایگان')
    pro = ('pro', 'پرو')
    enterprise = ('enterprise', 'شرکتی')


class Organization(BaseModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_owner')
    members = models.ManyToManyField(User, related_name='organization_members', through='Membership')
    plan = models.CharField(max_length=20, choices=PlanChoices.choices, default=PlanChoices.free)

    class Meta:
        verbose_name = 'سازمان'
        verbose_name_plural = 'سازمان'
        db_table = 'organizations'

    def __str__(self):
        return self.name



class MemberShip(BaseModel):
    ROLE_CHOICES = [
        ('admin', 'ادمین'),
        ('manager', 'مدیر'),
        ('member','عضو'),
        ('viewer', 'بیننده'),]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'عضویت'
        verbose_name_plural = 'عضویت'
        db_table = 'memberships'
        unique_together = ('user','organization')

    def __str__(self):
        return self.role


