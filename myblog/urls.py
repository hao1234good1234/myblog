"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # 注意：导入 include
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),  # 主页
    path('admin/', admin.site.urls),  # 管理后台
    # 修改主路由，添加 blog 应用
    # 主路由用 `include()` 分发
    # 把 /blog/ 下的所有请求交给 blog.urls 处理，`/blog/``blog.urls` → `views.home`，`/blog/3/``blog.urls` → `views.post_detail(id=3)`
    # 博客路由
    path('blog/', include('blog.urls', namespace='blog')),  # 在主路由中设置命名空间

    # 认证路由
    path('accounts/', include('accounts.urls')),
]
# 开发环境下提供媒体文件服务，是通过Django提供文件，Django 处理文件很慢、不安全，生产环境需要使用NGINX来直接提供文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #加的这条规则就是：“`/media/` 开头的请求，去 `MEDIA_ROOT` 找文件”
