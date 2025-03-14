from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        try:
            import users.signals
        except ImportError:
            pass