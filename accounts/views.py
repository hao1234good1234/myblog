# 编写视图函数
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

# 创建登录视图
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password= password)
            if user is not None:
                login(request, user) # 登录成功，创建会话
                return redirect('blog:article_list') # 跳转到首页
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
# 自定义登出视图
def logout_view(request):
    logout( request) # 销毁会话
    return redirect('blog:article_list')

# 创建注册视图
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # 自动创建 User 自动加密密码 并保存到数据库
            login(request, user)  # 注册完自动登录
            return redirect('blog:article_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

class Password_Change_View(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/accounts/login/'
    template_name = 'accounts/password_change.html'