from apps.core.permission import BasePermission
from apps.organizations.models import Organization,MemberShip

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        action=view.action
        if action == 'create':
               organization_id=request.data.get('organization')
               try:
                  organization=Organization.objects.get(id=organization_id)
                  membership=organization.memberships.get(user=user)
               except MemberShip.DoesNotExist:
                   return False
               role=membership.role
               if role in ['admin','manager','member']:
                    return True
               return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        organization = obj.organization
        try:
           membership = organization.memberships.get(user=user)
        except MemberShip.DoesNotExist:
            return False
        role=membership.role
        action=view.action
        if role in ['admin','manager']:
            return True
        elif role == 'member':
            if action in ['list','update','retrieve','partial_update','create']:
                  return True
            else:
              return False
        elif role == 'viewer':
            if action in ['retrieve','list']:
                return True
            else:
              return False

        return False