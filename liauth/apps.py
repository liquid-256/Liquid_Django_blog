from django.apps import AppConfig


class LiauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'liauth'

    def ready(self):
        import liauth.signals