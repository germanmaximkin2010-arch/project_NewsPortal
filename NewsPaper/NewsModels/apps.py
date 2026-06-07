from django.apps import AppConfig


class NewsmodelsConfig(AppConfig):
    name = 'NewsModels'
    def ready(self):
        import NewsModels.signals
