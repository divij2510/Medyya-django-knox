from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate  # Unused import?
from posts.models import Post, Like
from users.models import UserProfile
from cloudinary.forms import CloudinaryFileField

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    """
    Deserializes Post model data, excluding the ID field.
    """
    post_image = CloudinaryFileField()

    class Meta:
        model = Post
        exclude = ['id']
        required_fields = ['post_image']
        write_only_fields = ['user']


# class ProfileFieldsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['profile_picture']

class PostViewSerializer(serializers.ModelSerializer):
    user_firstname = serializers.CharField(source='user.first_name')
    user_lastname = serializers.CharField(source='user.last_name')
    user = serializers.CharField(source='user.username')
    likes = serializers.SerializerMethodField()
    post_image = CloudinaryFileField()
    user_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_profile_picture', 'post_image', 'caption', 'created_at', 'likes', 'user_firstname', 'user_lastname']

    def get_likes(self, obj):
        return obj.likes_count
    
    def get_user_profile_picture(self, obj):
        user_profile = obj.user.userprofile
        if user_profile.profile_picture:
            return user_profile.profile_picture.url
        return None