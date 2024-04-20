from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import UserProfile, Connection
from cloudinary.forms import CloudinaryFileField

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        required_fields = ['email', 'username', 'password']
        read_only_fields = ['is_staff', 'is_superuser']

    def validate_email(self, value):
        '''Check if the email is already in use.'''
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address is already in use.")
        return value

    def validate_username(self, value):
        '''Check if the username is already in use.'''
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value

class UserLoginSerializer(serializers.Serializer):
    '''Serializer for the user authentication object.'''
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        required_fields = []

class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = CloudinaryFileField()
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        required_fields = []

    def update(self, instance, validated_data):
        profile_picture = validated_data.get('profile_picture', None)
        if profile_picture is not None:
            instance.profile_picture.save(profile_picture.name, profile_picture, save=True)

        return super().update(instance, validated_data)

class ProfileViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_first_name = serializers.SerializerMethodField()
    user_last_name = serializers.SerializerMethodField()
    connections = serializers.SerializerMethodField()
    profile_picture = CloudinaryFileField()

    class Meta:
        model = UserProfile
        exclude = ['id']
        required_fields = []

    def get_user(self, obj):
        '''Get the username of the user.'''
        return obj.user.username

    def get_user_first_name(self, obj):
        '''Get the full name of the user.'''
        return obj.user.first_name
    
    def get_user_last_name(self, obj):
        '''Get the full name of the user.'''
        return obj.user.last_name

    def get_connections(self, obj):
        '''Get the number of connections for the user.'''
        return obj.connections_count

class ConnectionSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        exclude = ['is_accepted', 'to_user']

    def get_from_user(self, obj):
        '''Get the username of the user initiating the connection.'''
        return obj.from_user.username
