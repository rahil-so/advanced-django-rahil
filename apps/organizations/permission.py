from apps.core.permission import BasePermission
from apps.organizations.models import Organization,MemberShip


class MembershipPermission(BasePermission):
    def has_permisssion(self,request,view):
        user = request.user
        action = view.action
        if action == 'create':
            organization_id=request.data.get('organization')
            try:
                organization=Organization.objects.get(id=organization_id)
            except Organization.DoesNotExist:
                return False
            try:
                membership= organization.memberships.get(user=user)
            except MemberShip.DoesNotExist:
                return False
            if membership.role in ['admin','manager']:
                return True
            elif membership.role in ['member','viewer']:
                return False
        if action == 'list':
               return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        organization=obj.organization
        action=view.action
        try:
           membership=organization.memberships.get(user=user)
        except MemberShip.DoesNotExist:
            return False
        role=membership.role
        if action == 'retrieve':
            return True
        if action in ['update','partial_update']:
            if role in ['admin','manager']:
                return True
            else:
                return False
        elif action == 'destroy':
            if role == 'admin':
                return True
            else:
                return False
        return False





