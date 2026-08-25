from rest_framework import request
from rest_framework.permissions import BasePermission
from apps.organizations.models import MemberShip
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.organizations.models import Organization

class TaskPermission(BasePermission):

    def has_permission(self,request,view):
         user = request.user
         action= view.action
         if action == 'create':
             project_id=request.data.get('project')
             project=Project.objects.get(id=project_id)
             membership=Organization.membership.get(user=user)
             role=membership.role



