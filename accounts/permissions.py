from rest_framework.permissions import IsAuthenticated


class PremiumUserPermission(IsAuthenticated):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        is_authenticated = super().has_permission(request, view)
        # Additionally check if the user has a active silver or gold subscription
        has_subscription = request.user.get_user_subscription()
        return is_authenticated and has_subscription
