from django import forms
from .models import Article



# 第一种表单：`forms.ModelForm` 模型表单（关联数据库模型） 创建文章、编辑资料
# ✅ Django 会自动：
#
# - 根据 `Article` 模型生成字段
# - 设置 `CharField` → `<input type="text">`
# - 设置 `TextField` → `<textarea>`
# - 添加必填验证
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_published', 'summary', 'cover'] # 要包含的字段
        exclude = ['author']   # 或者排除某些字段
        widgets = {
            'cover': forms.ClearableFileInput(),  # 自动带“清除”复选框
        }

    # 字段级验证：`clean_字段名()`
    def clean_title(self):
        title = self.cleaned_data['title']
        if '垃圾' in title:
            raise forms.ValidationError('标题不能包含敏感词')
        return title
    # 全局验证：`clean()`
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title and content and len(content) < 50:
            raise forms.ValidationError('内容不能少于 50 个字')


# 第二种表单：`forms.Form`普通表单（不关联模型）登录、搜索、联系表单
# 适用于不保存到数据库的场景，比如“联系表单”。
# 在视图中使用方式和 `ModelForm` 基本一样。
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='姓名')
    email = forms.EmailField(label='邮箱')
    message = forms.CharField(widget=forms.Textarea,label='留言')

    def clean_message(self):
        # form.cleaned_data` 是一个字典，包含了用户提交的、经过验证和清洗后的数据
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('留言数字不能小于 10 个字')
        return message


