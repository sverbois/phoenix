from django.views import generic

from .models import Course


class CoursesView(generic.ListView):
    template_name = "coaching/courses.html"

    paginate_by = 2

    def get_queryset(self):
        return Course.objects.order_by("title")


class CourseView(generic.DetailView):
    model = Course
    template_name = "coaching/course.html"
