from django.db import models
from account.models import Account

# Create your models here.
from django.conf import settings
from datetime import datetime


def upload_location(instance, filename):
    file_path = 'image/post/{author_id}/{title}-{datetiming}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename,
        datetiming=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    return file_path


def upload_video_location(instance, filename):
    file_path = 'video/post/{author_id}/{title}-{datetiming}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename,
        datetiming=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    return file_path


class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    videofile = models.FileField(
        upload_to=upload_video_location, null=True, blank=True)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updateddate_updated")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ManyToManyField(Account, related_name="likingUser")
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    @classmethod
    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    @classmethod
    def dislike(cls, post, disliking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)

    def getnooflikes(self):
        return self.user.count()

    def __str__(self):
        return str(self.post)
