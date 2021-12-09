from django.urls import path

from . import views

app_name = "coaching"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("dashboard", views.dashboard_view, name="dashboard"),
    path("courses", views.CoursesView.as_view(), name="courses"),
    path("courses/<int:pk>/", views.CourseView.as_view(), name="course"),
]
