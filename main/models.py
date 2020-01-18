from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings


# Create your models here.

class TutorialCategory(models.Model):
    category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default=1)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class TutorialSeries(models.Model):
    series = models.CharField(max_length=200)

    series_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Category",
                                        on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Tutorial Seriess in admin"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.series


class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=timezone.now())
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    tutorial_categories = models.ForeignKey(TutorialCategory, default=1, verbose_name="Categories",
                                            on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200, default=1)
    tutorial_uploader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE)
    file = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default.png")
    videofile = models.FileField(upload_to='videos', null=True, verbose_name="video", blank=True)

    def __str__(self):
        return self.tutorial_title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='')
    website = models.URLField(max_length=200, default='')
    phone = models.IntegerField(default=0)
    city = models.CharField(max_length=200, default="新日暮里")

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class UserProfileManager(models.Manager):
    pass


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE, null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)


class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="profile_images", blank=True, default="profile_images/default.png")

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def __str__(self):
        return self.user.username


def create_avatar(sender, **kwargs):
    if kwargs['created']:
        user_avatar = Photo.objects.create(user=kwargs['instance'])


post_save.connect(create_avatar, sender=User)


class Github(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=200, default='')
    github_password = models.CharField(max_length=200, default='')


def create_github(sender, **kwargs):
    if kwargs['created']:
        user_github = Github.objects.create(user=kwargs['instance'])


post_save.connect(create_github, sender=User)


class UserMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=2000)
    message = models.TextField()


class Comment(models.Model):
    comment = models.TextField()
    comment_id = models.FloatField(max_length=100, default=0, primary_key=True)
    comment_time = models.DateTimeField(auto_now=True)
    tutorial = models.ForeignKey(Tutorial, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE, null=True)
