from django.urls import path
from . import views
from .views import Password_Change_View
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# 创建应用的分路由
urlpatterns = [
    path('login/', views.login_view, name='login'), # 登录视图
    path('logout', LogoutView.as_view(next_page = 'article_list'), name='logout'), # 使用Django自带的登出视图
    # path('logout/', views.logout_view, name='logout'),  # 自定义登出视图
    path('register/', views.register_view, name='register'),  # 注册视图
    path('password-change/', Password_Change_View.as_view(), name='password_change'), # 修改密码

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]