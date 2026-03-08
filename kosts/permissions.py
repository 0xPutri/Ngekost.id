from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def hasattr_owner(self, obj):
        if hasattr(obj, 'owner'):
            return obj.owner
        elif hasattr(obj, 'kost'):
            return obj.kost.owner
        return None
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'owner'
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        owner = self.hasattr_owner(obj)
        return owner == request.user