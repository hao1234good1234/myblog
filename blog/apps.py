from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    # 在 `apps.py` 的 `ready()` 中导入 `signals` 模块
    def ready(self):
        import blog.signals  # ← 关键！导入 signals 模块
