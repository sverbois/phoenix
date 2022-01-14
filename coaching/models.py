from datetime import date
from datetime import datetime

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

    def next_sessions(self):
        now = datetime.now()
        return self.session_set.filter(start__gt=now).order_by("start")


class Session(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    inscriptions = models.ManyToManyField(User, through="Inscription")
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f"{self.course.title} / {self.start}"


# Documentation : https://docs.djangoproject.com/en/3.2/topics/db/models/#extra-fields-on-many-to-many-relationships
class Inscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # https://docs.djangoproject.com/en/3.2/ref/models/constraints/#uniqueconstraint
            models.UniqueConstraint(
                fields=["session", "user"], name="inscription_unique_user_session"
            )
        ]

    def __str__(self):
        return f"{self.user} / {self.session}"


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
