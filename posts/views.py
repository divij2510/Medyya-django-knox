from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .models import Post, Like
from .serializers import PostSerializer, PostViewSerializer  # Explicitly import serializers


class CreatePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        """
        Creates a new post.
        """  

        request_data = request.data.copy()
        request_data['user'] = request.user.id

        serializer = PostSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, post_id):
        """
        Deletes a post owned by the authenticated user.
        """  

        try:
            post = Post.objects.get(id=post_id, user=request.user)
            post.delete()
            return Response({'message': 'Post Deleted successfully'}, status=status.HTTP_410_GONE)
        except Post.DoesNotExist:
            return Response({'error': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class PostsListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves a list of all posts.
        """  

        posts = Post.objects.all()
        serializer = PostViewSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Likes a post if the user hasn't already liked it.
        """  

        post = Post.objects.get(id=post_id)

        try:
            Like.objects.get(user=request.user, post=post)
            return Response({'error': 'Like on this Post already exists'})
        except Like.DoesNotExist:
            Like.objects.create(user=request.user, post=post)
            return Response({'message': 'Post Liked Successfully'}, status=status.HTTP_201_CREATED)


class UnlikePostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Unlikes a post if the user has already liked it.
        """  

        post = Post.objects.get(id=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'message': 'Post Unliked Successfully'}, status=status.HTTP_410_GONE)
        except Like.DoesNotExist:
            return Response({'error': 'Like on this Post does not exist'})
