from django.urls import path

from . import views

app_name = "coaching"
urlpatterns = [
    path("courses", views.CoursesView.as_view(), name="courses"),
    path("courses/<int:pk>/", views.CourseView.as_view(), name="course"),
]
