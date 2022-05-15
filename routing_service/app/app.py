from app.management import ApiManager
from app.settings import conf


app_manager = ApiManager(config=conf)
app_instance = app_manager.app_instance
