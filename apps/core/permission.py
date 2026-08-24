from rest_framework.permissions import BasePermission


class BaseModelPermission(BasePermission):
     def has_object_permission(self,request,view,obj):
         user=request.user
         owner=obj.owner
         if user == owner:
             return True
         else:
             return False
