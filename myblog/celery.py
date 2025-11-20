import os
from celery import Celery
# 设置django默认配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
app = Celery('myblog')

# 从settings.py 中加载以 CELERY_ 开头的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现各 app 下的tasks.py
app.autodiscover_tasks()
