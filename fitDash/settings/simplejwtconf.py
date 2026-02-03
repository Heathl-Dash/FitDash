import os

KEYCLOAK_URL = os.environ.get("KEYCLOAK_SERVER_REALM_URL", "http//localhost:8080")

SIMPLE_JWT = {
    "ALGORITHM": "RS256",
    "JWK_URL": f"{KEYCLOAK_URL}/protocol/openid-connect/certs",
    "AUTH_HEADER_TYPES": ("Bearer",),

    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",

    "AUTH_TOKEN_CLASSES": ("fitCore.api.permission_classes.KeycloakAccessToken",),
}
