from django.contrib import admin
from .models import Post, Topic, Comment
# Register your models here.
# admin.site.register(Post)
admin.site.register(Topic)
# admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False  # Deny edit permission for all users


class CommentAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False  # Deny edit permission for all users


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
