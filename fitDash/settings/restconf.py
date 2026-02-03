REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "fitCore.api.permission_classes.DashboardJWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

CORS_ORIGIN_ALLOW_ALL = True
