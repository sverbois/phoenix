from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ContactForm


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]
            recipients = ["sebastien.verbois@gmail.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            messages.success(
                request, f"Votre demande d'information a bien été envoyée."
            )
            return HttpResponseRedirect("/")
    else:  # GET
        form = ContactForm()
    return render(request, "phoenix/contact.html", {"form": form})
