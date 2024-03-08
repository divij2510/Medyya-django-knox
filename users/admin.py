from django.contrib import admin
from .models import UserProfile, Connection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture', 'slug', 'bio', 'display_connections_count', 'user__id']
    search_fields = ['user__username', 'user__slug']
    empty_value_display = '--not available--'
    
    #To get property connections_count from UserProfile model:
    def display_connections_count(self, obj):
        return obj.connections_count
    def user__id(self, obj):
        return obj.user.id
    display_connections_count.short_description = 'Connections Count'

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'created_at', 'is_accepted']
    list_filter = ['is_accepted']
    search_fields = ['from_user__username', 'to_user__username']
