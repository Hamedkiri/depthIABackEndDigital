from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from store.models import User



class MyBackend(BaseBackend):
    def authenticate(self, request,email=None,password=None,is_staff=None):
        if email is None or password is None:
            return None
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) is True:
               return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



