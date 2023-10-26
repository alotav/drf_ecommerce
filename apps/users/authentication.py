from datetime import timedelta
from django.utils import timezone

from django.settings import TOKEN_EXPIRED_AFTER_SECONDS

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
    

class ExpiringTokenAuthentication(TokenAuthentication):

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expired_handler(self,token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            print('Token expirado.')

        return is_expire

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Token Invalido.')

        if not token.user.is_active:
            raise AuthenticationFailed('Usuario no activo o eliminado.')

        is_expired = token_expired_handler(token)
        if is_expired:
            raise AuthenticationFailed('Su token ha expirado.')

        return (token.user, token)