from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/", default='avatar.png')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_title = models.CharField(max_length=50)
    tweet_text = models.CharField(max_length=280)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.author}: {self.tweet_title}"


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Request(models.Model):
    ip_address = models.GenericIPAddressField()
    last_request_time = models.TimeField()
    num_of_requests = models.IntegerField(default=1)
    black_list = models.BooleanField(default=False)

    def __str__(self):
        return self.ip


class UnAuthorizedRequests(models.Model):
    ip_address = models.GenericIPAddressField()
    num_of_requests = models.IntegerField(default=1)
    black_list = models.BooleanField(default=False)
    user = models.OneToOneField(User, related_name='requested_user', on_delete=models.CASCADE)


class FailedLogInAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    num_of_requests = models.IntegerField(default=1)
