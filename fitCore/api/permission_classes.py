# authentication.py (no Todo Service)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class DashboardJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            user_id = validated_token.get("sub")

            if not user_id:
                raise AuthenticationFailed("Token sem identificador 'sub'")

            return (ProfileDash(user_id, validated_token), validated_token)
        except InvalidToken as e:
            raise AuthenticationFailed(str(e), code="invalid_token")


class ProfileDash:
    def __init__(self, user_id, payload):
        self.id = user_id
        self.is_authenticated = True
        payload = payload


class KeycloakAccessToken(AccessToken):
    token_type = "access"

    def verify_token_type(self):
        pass
