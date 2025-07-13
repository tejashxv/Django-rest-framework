from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied 


class OwnerPermission(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object
        return obj.user == request.user

    def has_permission(self, request, view):
        # Allow any authenticated user to access the view
        return request.user and request.user.is_authenticated
    
    
    
class IsVIPuser(BasePermission):
    """
    Custom permission to only allow VIP users to access certain views.
    """
    
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.extended_profile.is_vip:
             return True
        raise PermissionDenied("You must be a VIP user to access this resource.")
