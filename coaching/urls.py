from django.urls import path

from . import views

app_name = "coaching"
urlpatterns = [
    path("", views.home_view, name="home"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("courses", views.CoursesView.as_view(), name="courses"),
    path("courses/<int:pk>/", views.CourseView.as_view(), name="course"),
    path("inscription", views.inscription_view, name="inscription"),
    path(
        "delete-inscription/<int:pk>/",
        views.DeleteInscription.as_view(),
        name="delete-inscription",
    ),
]
