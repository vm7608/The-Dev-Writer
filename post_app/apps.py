from django.apps import AppConfig


class PostAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post_app'

    def ready(self) : 
        from django.contrib.staticfiles import finders
        finders.find('post_app\static\article\script.js')
