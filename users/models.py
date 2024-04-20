from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('profile_pictures', default='http://res.cloudinary.com/dk3tpyyee/image/upload/v1713565892/bpwwih53rqle48wt7bsw.png', transformation={
            'quality': 'auto:low', 'fetch_format':'auto'
        })
    bio = models.TextField(blank=True, null=True, default='Hey there, I just joined Medyya')
    # slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        '''Return a string representation of the user profile.'''
        return self.user.username

    @property
    def connections_count(self):
        '''Calculates the total number of accepted connections for the user.'''
        from_connections_count = Connection.objects.filter(from_user=self.user, is_accepted=True).count()
        to_connections_count = Connection.objects.filter(to_user=self.user, is_accepted=True).count()
        return from_connections_count + to_connections_count


class Connection(models.Model):
    from_user = models.ForeignKey(User, related_name='outgoing_connections', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='incoming_connections', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def clean(self):
        '''Validates that a connection doesn't already exist in the reverse direction.'''
        if Connection.objects.filter(from_user=self.to_user, to_user=self.from_user).exists():
            raise ValidationError('A Connection already exists between the two users.')

    def save(self, *args, **kwargs):
        '''Override the save method to perform validation before saving.'''
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        '''Return a string representation of the connection.'''
        return f'{self.from_user} to {self.to_user}'
