from django import forms
from django.core.exceptions import ValidationError


class ContactForm(forms.Form):
    subject = forms.CharField(label="Sujet de votre demande", max_length=100)
    message = forms.CharField(
        label="Description de votre demande", widget=forms.Textarea
    )
    sender = forms.EmailField(label="Votre adresse gmail", initial="@gmail.com")
    cc_myself = forms.BooleanField(label="Me mettre en copie", required=False)

    def clean_sender(self):
        data = self.cleaned_data["sender"]
        if not data.endswith("@gmail.com"):
            raise ValidationError("Votre courriel n'est pas une adresse gmail.")
        return data
