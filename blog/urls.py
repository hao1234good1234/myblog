from django.urls import path
from . import views
from .views import HomeView, AboutView, ArticleListView, ArticleDetailView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# 创建应用的分路由
# `app_name = 'blog'` 告诉 Django：“这个 URL 集合属于 `blog` 应用”
app_name = 'blog'  # 如果要使用 <a href="{% url 'blog:article_list' %}">返回列表</a> 或 return redirect('blog:article_list') 必须加上这一行！
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('v1/', HomeView.as_view()),  #类视图必须用 `.as_view()` 转换为可调用的视图函数！
    path('about/', AboutView.as_view()),
    path('articles/', ArticleListView.as_view(), name='articles'), #name的作用是给路由起一个名字，方便后续引用。
    path('articles/<int:id>/', ArticleDetailView.as_view(), name='article_detail'),  # 这里的 id 必须和 ArticleDetailView中的pk_url_kwarg的值 id 名字对应一致！
    path('list/',views.article_list, name="article_list"), # 这个才是主页
    path('one/',views.article_one, name="article_one"),
    path('create/', views.create_article, name="create_article"),
    path('contact/', views.Contact, name="contact"),
    path('update/<int:id>/', views.update_article, name="update_article"),
    path('delete/<int:id>/', views.delete_article, name="delete_article"),
    path('publish/<int:id>/', views.publish_article, name="publish_article")
]