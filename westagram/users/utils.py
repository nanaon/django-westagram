from .models import Users
import jwt

def auth(func):
    def wrapper(self, request, **kwargs):
        auth_token = request.headers.get("Authorization")
        payload = jwt.decode(auth_token, 'secret')
        if Users.objects.get(id=payload['id']):
            user = Users.objects.get(id=payload['id'])
            request.user = user
        return func(self, request, **kwargs)
    return wrapper


