from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import  cache
from .models import Article
from django.core.mail import send_mail
import django.dispatch
@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def clear_article_cache(sender, **kwargs):
    """
    当文章保存或删除时，清除相关缓存
    """
    print("清除文章列表缓存...")

    # 清除所有文章列表缓存
    # cache.delete("blog:article_list")
    # 清除当前用户的文章列表缓存
    # cache.delete(f"blog:{kwargs['instance'].author.id}:article_list")
    # 如果需要，也可以清除所有用户的缓存（按需设计）
    cache.delete_pattern("blog:*:article_list") # django-redis特有的方法，需要下载django-redis库
@receiver(post_save, sender=Article)
def handle_article_save(sender, instance, created, **kwargs):
    if created: # `created=True` 表示是新建对象。
        print(f"新文章创建: {instance.title}")
        # 新文章发通知（仅创建时）
        if instance.is_published:
            send_mail(
                subject="新文章发布了",
                message=f"快来看{instance.title}",
                from_email="admin@myblog.com",
                recipient_list=['editor@myblog.com'],
                fail_silently=True,
            )

    else:
        print(f"文章更新: {instance.title}")


# ====== 2. 自定义信号：用户点赞 ======
# 定义信号（通常放在顶部）
user_liked = django.dispatch.Signal()
@receiver(user_liked)
def send_like_notification(sender, user, article, **kwargs):
    print(f"{user}点赞了{article.title}")
    # 这里可以发站内信、邮件、WebSocket 通知等

