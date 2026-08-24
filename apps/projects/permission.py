from core.permission import BasePermission

class ProjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        organization = obj.organization
        membership = organization.memberships.get(user=user)
        role=membership.role
        action=view.action
        if role in ['admin','manager']:
            return True
        elif role == 'member':
            if action == 'update,retrieve,partial_update,create':
                  return True
            else:
              return False
        elif role == 'viewer':
            if action == 'retrieve':
                return True
            else:
              return False
        else:
            return False

