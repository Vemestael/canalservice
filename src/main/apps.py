from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        """
        Вызывает обновление данных из таблицы при каждом запуске сервера
        """
        from main.views import GSheetsAPI
        GSheetsAPI().get('')
