from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # Unused import?
from posts.models import Post, Like
from users.models import UserProfile


class PostSerializer(serializers.ModelSerializer):
    """
    Deserializes Post model data, excluding the ID field.
    """

    class Meta:
        model = Post
        exclude = ['id']
        required_fields = ['post_image']
        write_only_fields = ['user']


class PostViewSerializer(serializers.ModelSerializer):
    """
    Serializes Post model data with additional fields for user-related information.
    """

    user_slug = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user_slug(self, obj):
        """
        Retrieves the user profile slug for the post's author.
        """
        user_profile = UserProfile.objects.get(user=obj.user)
        return user_profile.slug

    def get_likes(self, obj):
        """
        Returns the number of likes for the post.
        """
        return obj.likes_count

    def get_user(self, obj):
        """
        Returns the username of the post's author.
        """
        return obj.user.username
