from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Course
from .models import Inscription
from .models import Profile
from .models import Session


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ProfileUserAdmin)


class SessionInline(admin.TabularInline):
    model = Session
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Cours",
            {
                "fields": [
                    "title",
                    "description",
                    "max_attendees",
                    "min_age",
                    "image",
                    "teacher",
                ],
                "classes": ["collapse"],
            },
        ),
    ]
    inlines = [SessionInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Inscription)
