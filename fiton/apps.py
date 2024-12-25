from django.apps import AppConfig


class FitonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fiton'

    def ready(self):
        import fiton.signals
