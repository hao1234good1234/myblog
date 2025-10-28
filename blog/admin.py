from django.contrib import admin
from .models import Article


@admin.register(Article)  # 注册 Article 模型到管理后台
class ArticleAdmin(admin.ModelAdmin):
    # 在文章列表页显示的字段
    list_display = ('title', 'content', 'is_published', 'created_time')

    # 点击标题进入详情
    list_display_links = ('title',)

    # 列表页直接编辑
    list_editable = ('is_published',) #在列表页直接勾选“是否发布”，无需点进详情！

    # 右侧边栏的过滤器，可以按这些字段筛选文章
    list_filter = ('is_published', 'created_time', 'author')

    # 搜索框可以搜索的字段
    search_fields = ('title', 'content', 'author__username')

    # 排序 负号 `-` 表示倒序。
    ordering = ['-created_time']

    # 简单控制字段顺序
    # 添加/编辑文章时显示的字段
    # fields = ('title', 'content', 'author', 'is_published', 'summary')

    # 高级分组显示：
    fieldsets = [
        (None, {'fields': ('title', 'content')}),
        ('高级设置', {'fields': ('summary', 'author', 'is_published'),
                      'classes': ('collapse',) # 可折叠
                      }),
    ]

    # 只读字段 防止误改
    readonly_fields = ('created_time', 'updated_time')  # 只读
    # 分页
    list_per_page = 10
    # 顶部出现日期导航
    date_hierarchy = 'created_time'
    # 自动填充slug
    # prepopulated_fields = {'slug': ('title',)} #输入标题时，`slug` 自动变成 `my-awesome-article`
