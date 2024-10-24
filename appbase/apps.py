from django.apps import AppConfig
from pkg_helpers.services.service_name import USER_SERVICE

class AppbaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appbase'
    api_prefix = f"{USER_SERVICE}/"
