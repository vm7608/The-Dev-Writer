from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    # This is the name of the app as it appears in the admin panel

    def ready(self):
        import user_app.signals
