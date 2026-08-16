import logging

from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render

from .forms import EmailForm


logger = logging.getLogger(__name__)

"""
Logic was written by Milana and Garv but Princess needed to re-merge into maestro manually
"""

def send_email_view(request):
    """
    Display the email form and send an email when valid form data is submitted.
    """

    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():
            sender_email = form.cleaned_data["sender_email"]
            recipient_email = form.cleaned_data["recipient_email"]
            cc_emails = form.cleaned_data["cc_emails"]
            subject = form.cleaned_data["subject"]
            message_body = form.cleaned_data["message"]
            attachments = form.cleaned_data["attachments"]

            try:
                email = EmailMessage(
                    subject=subject,
                    body=message_body,
                    from_email=None,
                    to=[recipient_email],
                    cc=cc_emails,
                    reply_to=[sender_email],
                )

                # Add all uploaded attachments to the email.
                for attachment in attachments:
                    email.attach(
                        attachment.name,
                        attachment.read(),
                        attachment.content_type,
                    )

                # Send the email through the configured SMTP server.
                email.send(fail_silently=False)

                messages.success(
                    request,
                    "Email sent successfully!"
                )

                # Clear the form after successful sending.
                form = EmailForm()

            except Exception as error:
                logger.exception("Email sending failed.")

                messages.error(
                    request,
                    f"Failed to send email: {error}"
                )

    else:
        form = EmailForm()

    return render(
        request,
        "email_app/send_email.html",
        {"form": form}
    )