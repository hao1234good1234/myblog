from .celery import app as celery_app
__all__ = ('celery_app',) # 这样 Django 启动时会自动加载 Celery。
