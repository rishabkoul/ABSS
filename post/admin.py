from django.contrib import admin
from post.models import Post, Like
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    ordering = ['-date_updated']
    search_fields = ('title', 'body')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
