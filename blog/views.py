# 编写视图函数
from http.client import responses

from django.http import HttpResponse
from django.template.context_processors import request
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Article
from datetime import datetime, timedelta
from .forms import ArticleForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

def home(request):
    return HttpResponse("这是博客系统首页！")
def post_detail(request, id):
    return HttpResponse(f"这是第{id}篇文章")
def index(request):
    context = {
        'title': '首页',
        'posts': ['文章1', '文章2', '文章3']
    }
    return render(request, 'blog/home.html', context)

@method_decorator(csrf_exempt, name='dispatch')  #暂时关闭 CSRF 检查,生产环境不要用！容易被攻击！
class HomeView(View):
    # http_method_names = ['get', 'post']   # ✅ 显式允许 POST
    def get(self, request):
        return HttpResponse("这是 get 请求")
    def post(self, request):
        return HttpResponse("这是 post 请求")

class AboutView(TemplateView):
    template_name = 'blog/about.html'  # 指定模板文件
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '关于我们'
        context['posts'] = ['电话', '邮箱', '许可证']
        return context

class ArticleListView(ListView):
    model = Article              # 指定模型
    template_name = 'blog/article_list.html'  # 自定义模板
    context_object_name = 'articles' # 模板中用的变量名
    paginate_by = 3 # 分页：每页5条

class ArticleDetailView(DetailView):
    model = Article              # 指定模型
    template_name = 'blog/article_detail.html'  # 自定义模板
    context_object_name = 'article' # 模板中用的变量名
    pk_url_kwarg = 'id'  # 如果 URL 中是 <int:id>

def article_list(request):
    # 返回的是QuerySet，它的特点有：
    # 1. 惰性求值，查询不会立即执行，真的需要的时候再执行，避免不必要的查询。
    # 2. 链式调用， 每个方法都返回一个新的 QuerySet，可以继续调用。
    # articles = Article.objects.filter(is_published=True).filter(author_id=1).order_by('-created_time') # '-'代表降序
    # 3. 切片，实现分页,  类似 SQL 的 `LIMIT` 和 `OFFSET`
    # articles = Article.objects.all()[:2] # 获取前2个对象
    # articles = Article.objects.all()[5:10]
    # 4. 排序 负号 `-` 表示倒序。
    # articles = Article.objects.order_by('-created_time') # 按创建时间倒序（最新在前）
    # articles = Article.objects.order_by('title')  # 按标题升序
    # articles = Article.objects.order_by('is_published', '-created_time')


    #方法1：all
    articles = Article.objects.all() # 获取所有对象

    #方法2：filter ,支持 `__` 双下划线语法，比如 `author__username` 表示“作者的用户名”
    # articles = Article.objects.filter(is_published=True)    #过滤符合条件的对象
    # articles = Article.objects.filter(author__username='admin') # 按作者过滤
    # today = datetime.now().date()
    # articles = Article.objects.filter(created_time__date=today) # 按创建时间过滤
    # articles = Article.objects.filter(created_time__gt=today) # 创建时间 大于 / 大于等于 当前时间
    # articles = Article.objects.filter(is_published=False, author_id=1)
    # articles = Article.objects.filter(author=request.user) #某用户的全部文章
    # articles = Article.objects.order_by('-created_at')[:5]  # 最新的5篇
    # articles = Article.objects.filter(title__contains='Django') #包含“Django”的文章
    # articles = Article.objects.filter(title__icontains='Django') #不区分大小写的包含“Django”的文章
    # articles = Article.objects.filter(title__startswith='Python')  #标题以“Python”开头
    # articles = Article.objects.filter(summary__isnull=True) # 没有摘要的文章

    # 方法3：exclude
    # articles = Article.objects.exclude(is_published=True)
    # articles = Article.objects.exclude(author__username__in=['Alice', 'test'])
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_one(request):
    article = Article.objects.get(pk=3)  #获取唯一一个对象, pk是主键
    return render(request, 'blog/article_detail.html', {'article': article})


# 在视图中使用表单
#  这就是经典的 **“GET 显示，POST 处理”** 模式。


# 用 `@login_required` 装饰器！登录后才能访问
# - 未登录用户访问 `/create/` → 自动跳转到登录页
# - 登录成功后 → 自动回到 `/create/`
@login_required
def create_article(request):
    user = request.user
    print(f"现在登录的用户是：{user}")
    if request.method == 'POST':
        # 用户提交数据，绑定表单
        form = ArticleForm(request.POST)
        if form.is_valid():
            # 验证通过
            article = form.save(commit=False) # 先不保存
            article.author = request.user # 设置作者
            article.save() # 保存到数据库
            return redirect('article_list') # 重定向到列表页，articles是路由别名

    else:
        # GET 请求，显示空表单
        form = ArticleForm()
    return render(request, 'blog/create_article.html', {'form': form})

def Contact(request):
    if request.method == "POST":
        # 用户提交了表单，绑定数据
        form = ContactForm(request.POST)
        if form.is_valid():
            # 验证通过！
            # 注意：普通表单没有 .save() 方法
            # 你需要手动处理数据，比如：
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # 这里可以：
            # - 发送邮件
            # - 保存到数据库（如果需要）
            # - 记录日志等

            # 示例：打印到控制台
            print(f"收到留言：{name} ({email}) 说：{message}")
            # 处理完成后重定向，防止重复提交
            return redirect('home')  # 假设你有一个成功页面
    else:
        # GET 请求，显示空表单
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})
