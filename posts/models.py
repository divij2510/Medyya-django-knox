from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = CloudinaryField('post_images', blank=False, null=False, transformation={
            'quality': 'auto:eco'
        })
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Property to count the number of likes for a post
    @property
    def likes_count(self):
        '''Calculate and return the number of likes for this post.'''
        return self.likes.count()

    def __str__(self):
        '''Return a string representation of the post.'''
        return f'{self.user.username} - {self.created_at}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        '''Return a string representation of the like.'''
        return f'{self.user.username} liked {self.post}'
