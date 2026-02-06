from blog.models import Blog, Comment
from django.contrib import admin

admin.site.register(Comment)

class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine
    ]