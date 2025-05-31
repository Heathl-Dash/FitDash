REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'fitCore.api.permission_classes.DashboardJWTAuthentication',

    ),
    
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}