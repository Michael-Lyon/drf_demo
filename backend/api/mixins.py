from rest_framework import permissions  

from .permissioins import IsStaffEditorPermission


class StaffEditorPeermissionMixin():
    permission_classes = [
        permissions.IsAdminUser,
        IsStaffEditorPermission
    ]
    
class UserQuerySetMixin():
    allow_saff_view = False
    user_field = 'user'
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if self.allow_saff_view and  user.is_staff:
            return qs
        return qs.filter(**lookup_data)