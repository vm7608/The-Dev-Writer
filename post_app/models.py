from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # post_pics folder is created in media folder
    image = models.ImageField(
        default='post_default.jpg', upload_to='post_pics')
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    # rescale post image to 850x478

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 850 or img.width > 478:
            output_size = (850, 478)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def is_saved_by(self, user):
        return self.savepost_set.filter(user=user).exists()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
    

class SavePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.post.title