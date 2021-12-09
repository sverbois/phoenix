from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from .models import Course


def home_view(request):
    context = {}
    return render(request, "coaching/home.html", context)


@login_required
def dashboard_view(request):
    context = {}
    return render(request, "coaching/dashboard.html", context)


class CoursesView(generic.ListView):
    template_name = "coaching/courses.html"

    paginate_by = 2

    def get_queryset(self):
        return Course.objects.order_by("title")


class CourseView(generic.DetailView):
    model = Course
    template_name = "coaching/course.html"
