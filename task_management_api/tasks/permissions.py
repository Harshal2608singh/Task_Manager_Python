from rest_framework.permissions import BasePermission
from .models import UserProfile

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        profile = UserProfile.objects.get(user=request.user)
        return profile.role in ['ADMIN', 'MANAGER']
