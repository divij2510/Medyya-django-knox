from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView, LogoutView
from knox.auth import TokenAuthentication
from .serializers import *
from django.contrib.auth import login
from django.contrib.auth.models import User
from users.models import UserProfile, Connection

class UserRegistrationAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Activate user directly after successful registration
            user.is_active = True
            password = request.data.get('password')
            user.set_password(password)  
            user.save()
            # Create a blank profile for the new user
            UserProfile.objects.create(user=user)
            return Response({'user': serializer.validated_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(LoginView):
    serializer_class = UserLoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Check if user already has been assigned a knox token and delete it
        try:
            previous_token = AuthToken.objects.get(user=user)
            previous_token.delete()
        except AuthToken.DoesNotExist:
            pass
        # Assigning user a session and Calling the prewritten post method in knox app
        login(request, user)
        return super(UserLoginAPIView, self).post(request, format=None)     
    
class UserLogoutAPIView(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 
    def post(self, request, format=None):
        #Calling the prewritten logout post method
        return super(UserLogoutAPIView, self).post(request, format=None)

class UserProfileDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        # Check if user has a profile
        print(request.data)
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles = UserProfile.objects.all()
        serializer = ProfileViewSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        
        try:
            if username=='mine':
                profile = UserProfile.objects.get(user = request.user)
            else:
                profile = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProfileViewSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MakeConnectionRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if to_user == request.user:
            return Response({"error": "You cannot send a connection request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a connection request already exists
        if Connection.objects.filter(from_user=request.user, to_user=to_user).exists() or Connection.objects.filter(from_user=to_user, to_user=request.user).exists():
            return Response({"error": "Connection request already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new connection request
        connection = Connection(from_user=request.user, to_user=to_user)
        connection.save()
        return Response({"message": "Connection request sent successfully"}, status=status.HTTP_201_CREATED)

class AcceptConnectionRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            connection = Connection.objects.get(from_user=User.objects.get(username=username), to_user=request.user)
        except Connection.DoesNotExist:
            return Response({"error": "Connection request not found"}, status=status.HTTP_404_NOT_FOUND)

        if connection.is_accepted:
            return Response({"error": "Connection request has already been accepted"}, status=status.HTTP_400_BAD_REQUEST)

        connection.is_accepted = True
        connection.save()

        return Response({"message": "Connection request accepted successfully"}, status=status.HTTP_200_OK)

class DeclineConnectionRequestAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            connection = Connection.objects.get(from_user=User.objects.get(username=username), to_user=request.user)
        except Connection.DoesNotExist:
            return Response({"error": "Connection request not found"}, status=status.HTTP_404_NOT_FOUND)

        if connection.is_accepted:
            return Response({"error": "Connection request has already been accepted"}, status=status.HTTP_400_BAD_REQUEST)

        connection.delete()        
        return Response({"message": "Connection request declined"}, status=status.HTTP_200_OK)

class ConnectionRequestsListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        connection_requests = Connection.objects.filter(to_user=request.user, is_accepted=False)
        serializer = ConnectionSerializer(connection_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class ListRecommendedProfilesAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Getting all user's connection user ids
        connections = list(Connection.objects.filter(to_user=request.user, is_accepted=True).values_list('from_user', flat=True))
        connections += list(Connection.objects.filter(from_user=request.user, is_accepted=True).values_list('to_user', flat=True))
        # Getting the connections of the above connections, and excluding the user 
        mutual_connections = list(Connection.objects.filter(to_user__id__in=connections).values_list('from_user', flat=True)) + list(Connection.objects.filter(from_user__id__in=connections).values_list('to_user', flat=True))
        mutual_connections.remove(request.user.id)
        # Get profiles of these mutual connections
        try:
            recommended_profiles = UserProfile.objects.filter(user__id__in=mutual_connections)
            serializer = ProfileViewSerializer(recommended_profiles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'exception':'recommended profile does not exist'})