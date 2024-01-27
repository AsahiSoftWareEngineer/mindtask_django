import os
import secrets
import jwt

from accounts.models import User
from django.conf import settings


class Account:
    def getUserId(self, access_token):
        SECRET_KEY:str = getattr(settings, 'SECRET_KEY', None)
        payload:dict = jwt.decode(jwt=access_token, key=SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]