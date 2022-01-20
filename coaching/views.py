from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views import generic
from django.views.generic.edit import DeleteView

from .models import Course
from .models import Inscription


def home_view(request):
    context = {}
    return render(request, "coaching/home.html", context)


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        self.request = request
        context = {
            "next_inscriptions": self.get_next_inscriptions(),
            "next_sessions": self.get_next_sessions(),
        }
        return render(request, "coaching/dashboard.html", context)

    def get_next_inscriptions(self):
        now = datetime.now()
        current_user = self.request.user
        inscriptions = (
            Inscription.objects.filter(user=current_user)
            .filter(session__start__gt=now)
            .order_by("session__start")
        )
        return inscriptions

    def get_next_sessions(self):
        inscriptions = self.get_next_inscriptions()
        return [ins.session for ins in inscriptions]


class CoursesView(generic.ListView):
    template_name = "coaching/courses.html"

    paginate_by = 2

    def get_queryset(self):
        return Course.objects.order_by("title")


class CourseView(generic.DetailView):
    model = Course
    template_name = "coaching/course.html"


@login_required
def inscription_view(request):
    user_id = request.user.id
    if request.method == "POST":
        session_id = request.POST["session_id"]
        old_inscription = (
            Inscription.objects.filter(user_id=user_id)
            .filter(session_id=session_id)
            .first()
        )
        if "add" in request.POST and not old_inscription:
            new_inscription = Inscription(user_id=user_id, session_id=session_id)
            new_inscription.save()
            messages.success(
                request, f"Votre inscription {new_inscription} a bien été enregistrée."
            )
        if "add" in request.POST and old_inscription:
            messages.warning(request, f"Vous êtes déjà inscrit à {old_inscription} .")
        if "delete" in request.POST and old_inscription:
            old_inscription.delete()
            messages.info(
                request, f"Votre inscription {old_inscription} a bien été effacée."
            )
    return HttpResponseRedirect(reverse("coaching:dashboard"))


class DeleteInscription(DeleteView):
    model = Inscription
    template_name = "coaching/delete-inscription.html"
    success_url = reverse_lazy("coaching:dashboard")
