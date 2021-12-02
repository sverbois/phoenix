from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField


class Course(models.Model):
    title = models.CharField(
        max_length=256,
    )
    description = models.TextField(
        blank=True,
    )
    max_attendees = models.IntegerField()
    min_age = models.IntegerField(
        blank=True,
        null=True,
    )
    image = VersatileImageField(
        upload_to="images/courses",
        blank=True,
        null=True,
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class Session(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.course.title} / {self.start}"


# TODO
# class Card(models.Model):
#    creation_date = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    curriculum = models.TextField(
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)
    instance.profile.save()
