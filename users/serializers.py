from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import UserProfile, Connection

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

class ProfileViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    connections = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        exclude = ['id']

    def get_user(self, obj):
        '''Get the username of the user.'''
        return obj.user.username

    def get_user_full_name(self, obj):
        '''Get the full name of the user.'''
        return obj.user.first_name + ' ' + obj.user.last_name

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
