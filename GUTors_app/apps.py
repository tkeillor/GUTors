from django.apps import AppConfig


class GutorsAppConfig(AppConfig):
    name = 'GUTors_app'

    def ready(self):
        import signals

