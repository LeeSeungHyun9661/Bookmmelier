from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# class MyUserBackend(ModelBackend):
#     def authenticate(self, request, **kwargs):
#         id = kwargs.get('id')
#         password = kwargs.get('password')
#         try:
#             user = User.objects.get(id=id)
#             if user.user.check_password(password) is True:
#                 return user.user
#         except user.DoesNotExist:
#             return None


class MyUserBackend(ModelBackend):
    def authenticate(self,request, **kwargs):
        id = kwargs.get('id')
        password = kwargs.get('password')
        try:
            user = get_user_model().objects.get(id=id)
        except Exception as e:
            print(e)
            raise Exception('Wrong ID')
        if user.check_password(password):
            return user
        else:
            raise Exception('Wrong Password')
