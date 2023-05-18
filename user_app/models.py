from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from post_app.models import SavePost, Vote
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pics folder is created in the media folder
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
            
    # get all posts id from post_app.models.SavePost
    def get_saved_posts(self):
        temp = SavePost.objects.filter(user=self.user)
        saved_posts = [post.post for post in temp]
        return saved_posts
    
    def get_upvoted_posts(self):
        temp = Vote.objects.filter(user=self.user, vote_type='Upvote')
        upvoted_posts = [post.post for post in temp]
        return upvoted_posts
    
    def get_downvoted_posts(self):
        temp = Vote.objects.filter(user=self.user, vote_type='Downvote')
        downvoted_posts = [post.post for post in temp]
        return downvoted_posts
