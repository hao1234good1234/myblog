from django.urls import path
from . import views
from .views import HomeView, AboutView, ArticleListView, ArticleDetailView
# 创建应用的分路由
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('v1/', HomeView.as_view()),  #类视图必须用 `.as_view()` 转换为可调用的视图函数！
    path('about/', AboutView.as_view()),
    path('articles/', ArticleListView.as_view(), name='articles'), #name的作用是给路由起一个名字，方便后续引用。
    path('articles/<int:id>/', ArticleDetailView.as_view(), name='article_detail'),  # 这里的 id 必须和 ArticleDetailView中的pk_url_kwarg的值 id 名字对应一致！
    path('list/',views.article_list, name="article_list"),
    path('one/',views.article_one, name="article_one"),
    path('create/', views.create_article, name="create_article"),
    path('contact/', views.Contace, name="contact"),
]