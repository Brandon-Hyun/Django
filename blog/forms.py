from django import forms
from django_summernote.widgets import SummernoteWidget
from blog.models import Blog,Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('category', 'title','image', 'content')
        widgets = {
            'content': SummernoteWidget()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        # 폼 필드가 렌더링될 때 사용할 HTML 위젯을 정의
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}) # 부트스트랩
        }
        labels = {
            'content': '댓글'
        }