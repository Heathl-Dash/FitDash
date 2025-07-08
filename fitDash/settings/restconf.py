REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'fitCore.api.permission_classes.DashboardJWTAuthentication',

    ),
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

CORS_ORIGIN_ALLOW_ALL=True