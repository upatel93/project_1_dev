from django.apps import AppConfig


class TicketkartappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketkartapp'

    def ready(self):
        import ticketkartapp.signals