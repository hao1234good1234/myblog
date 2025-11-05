from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题', help_text="请输入文章标题")
    content = models.TextField( verbose_name='正文', help_text='请输入文章内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_time = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE, verbose_name="作者")  # 关联作者，`on_delete=models.CASCADE`：用户删除时，他的文章也一起删除
    is_published = models.BooleanField(default=True, verbose_name="是否发布")

    summary = models.CharField(max_length=300, verbose_name='摘要(可选)', null=True, blank=True, help_text='请输入文章摘要')

    #上传图片
    # - `upload_to='covers/'`：文件会保存到 `MEDIA_ROOT/covers/`
    # - `blank=True, null=True`：允许不上传
    # cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面(可选)')

    def cover_path(self, filename):  # ← 改成类方法！
        author_id = getattr(self.author, 'id', 'unknown')
        return f'covers/{author_id}/{filename}'
    cover = models.ImageField(upload_to=cover_path, blank=True, null=True, verbose_name='封面(可选)')

    # 控制对象显示名
    # 默认情况下，Django 显示对象为 `Article object (1)`，不友好。我们用 `__str__()` 让它显示为文章标题
    # 在后台、调试、关联字段中都会显示标题，而不是 `Article object`。
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章(meta)'
        verbose_name_plural = '文章列表'  # 后台显示的复数名称
        ordering = ['-created_time'] # 按创建时间倒序排列, 负号表示倒序，最新的文章排在前面。
        db_table = 'blog_articles'  # 自定义表名（可选）
        permissions = [
            ("can_publish", "可以发布文章"),
            ("can_pin", "可以置顶文章"),
        ]

def cover_path(instance, filename):  # ← 没有 self！
    author_id = getattr(instance.author, 'id', 'unknown')
    return f'covers/{author_id}/{filename}'