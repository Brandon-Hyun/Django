from django.contrib import admin
from blog.models import Blog
# Register your models here.
@admin.register(Blog)
class BlojAdmin(admin.ModelAdmin):
    ...