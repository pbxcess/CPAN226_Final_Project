import logging

from django.shortcuts import render

from .forms import EmailForm

logger = logging.getLogger(__name__)


def send_email_view(request):
    """
    Display the email form and process submitted form data.

    Submitted values are currently printed to the console for testing.
    The email delivery functionality will be connected to this view
    through the project's email backend.
    """

    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():
            sender_email = form.cleaned_data["sender_email"]
            recipient_email = form.cleaned_data["recipient_email"]
            cc_emails = form.cleaned_data["cc_emails"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            attachments = form.cleaned_data["attachments"]

            # Temporary output used to verify that form data is received correctly.
            print("Sender:", sender_email)
            print("Recipient:", recipient_email)
            print("CC:", cc_emails)
            print("Subject:", subject)
            print("Message:", message)
            print("Attachments:", [attachment.name for attachment in attachments])

    # Form validation handles expected user errors. This view deliberately does
    # not send the email because SMTP delivery belongs to the back-end portion
    # of the group project. The validated attachment list is ready to pass to it.

    else:
        form = EmailForm()

    context = {
        "form": form
    }

    return render(request, "email_app/send_email.html", context)
