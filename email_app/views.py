from django.shortcuts import render

from .forms import EmailForm


def send_email_view(request):
    """Display the email form and process submitted form data."""

    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():
            sender_email = form.cleaned_data["sender_email"]
            recipient_email = form.cleaned_data["recipient_email"]
            cc_emails = form.cleaned_data["cc_emails"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            attachment = form.cleaned_data["attachment"]

            # Email sending functionality will be added next.
            print("Sender:", sender_email)
            print("Recipient:", recipient_email)
            print("CC:", cc_emails)
            print("Subject:", subject)
            print("Message:", message)
            print("Attachment:", attachment)

    else:
        form = EmailForm()

    context = {
        "form": form
    }

    return render(request, "email_app/send_email.html", context)