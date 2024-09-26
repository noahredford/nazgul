from django.core.exceptions import PermissionDenied

def user_is_property_manager(user):
    if user.role == 'PROPERTY_MANAGER':
        return True
    else:
        raise PermissionDenied