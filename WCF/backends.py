from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            user = User.objects.filter(email=username).order_by('id').first()
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
