from apps.core.permission import BasePermission
from apps.organizations.models import MemberShip
from apps.tasks.models import Task

class CommentPermission(BasePermission):
  def has_permission(self ,request ,view):
    user = request.user
    action =view.action
    if action=='create':
        task_id =request.data.get('task')
        try:
            task =Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return False
        project =task.project
        organization =project.organization
        try:
            memberships=organization.memberships.get(user=user)
        except MemberShip.DoesNotExist:
            return False
        role =memberships.role
        if role in ['admin' ,'member' ,'manager']:
            return True
        return False
    elif action in ['update','partial_update','destroy','list','retrieve']:
        return True
    return False

  def has_object_permission(self ,request ,view ,obj):
    user = request.user
    task =obj.task
    project =task.project
    organization =project.organization
    action =view.action
    try:
        memberships=organization.memberships.get(user=user)
    except MemberShip.DoesNotExist:
        return False
    role =memberships.role
    if action=='retrieve':
        return True
    elif action in ['update' ,'partial_update']:
        if role in ['admin' ,'manager'] or obj.author==user:
            return True
        else:
            return False
    elif action=='destroy':
        if role in ['admin' ,'manager'] or obj.author==user:
            return True
        else:
            return False
    return False