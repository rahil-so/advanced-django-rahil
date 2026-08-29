from enum import member

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
             try:
                 project = Project.objects.get(id=project_id)
             except Project.DoesNotExist:
                 return  False
             organization= project.organization
             try:
                 membership=organization.memberships.get(user=user)
             except MemberShip.DoesNotExist:
                  return False
             role = membership.role
             if role in ['admin', 'manager','member']:
                 return True
             else:
                 return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        project=obj.project
        organization=project.organization
        action= view.action
        try:
            membership=organization.memberships.get(user=user)
        except MemberShip.DoesNotExist:
            return False
        role=membership.role
        if action == 'retrieve':
            return True
        elif action in['update','partial_update']:
            if role in ['admin','manager','member']:
                return True
            else:
                return False
        elif action == 'destroy':
            if role in ['admin','manager']:
                return True
            else:
                return False
        return False










