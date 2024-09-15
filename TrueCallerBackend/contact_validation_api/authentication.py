from django.contrib.auth.backends import BaseBackend

from .models import AuthDetailStore


class Authentication(BaseBackend):
    @staticmethod
    def user_authentication(username, password):
        try:
            user = AuthDetailStore.objects.get(username=username, password=password)
            return user

        except RegisteredAppUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AuthDetailStore.objects.get(pk=user_id)
        except AuthDetailStore.DoesNotExist:
            return None
