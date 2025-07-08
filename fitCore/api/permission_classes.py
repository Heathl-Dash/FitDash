# authentication.py (no Todo Service)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class DashboardJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                return None

            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            user_id = validated_token.get('user_id') 

            if not user_id:
                raise ProfileDash("Token não contém user_id", code="no_user_id")

            return (ProfileDash(user_id), validated_token)

        except InvalidToken as e:
            raise AuthenticationFailed(str(e), code="invalid_token")

class ProfileDash:
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True 