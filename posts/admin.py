from django.contrib import admin
from .models import Post, Like

# Register your models here.

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['user', 'post_image', 'caption', 'likes_count', 'id']
    list_filter = ['user', 'created_at']
    search_fields = ['user__slug', 'user__username', 'caption']

    # Calculating number of likes to display in admin panel
    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = 'Likes'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['user__username', 'post__caption']
