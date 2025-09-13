from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsFarmerOrReadOnly(BasePermission):
    """
    - Any logged-in user can view (GET/HEAD/OPTIONS).
    - Only farmers can create/update/delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  

        if request.method in SAFE_METHODS:
            return True  

        return hasattr(request.user, "profile") and request.user.profile.role == "farmer"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner.user == request.user


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "profile")
            and request.user.profile.role == "buyer"
        )
