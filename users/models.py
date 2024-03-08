from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default_pic.png')
    bio = models.TextField(blank=True, null=True, default='Hey there, I just joined Medyya')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        '''Return a string representation of the user profile.'''
        return self.user.username

    def save(self, *args, **kwargs):
        '''Override the save method to automatically generate a slug if it's not provided.'''
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

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
