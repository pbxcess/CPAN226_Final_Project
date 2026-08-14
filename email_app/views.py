from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render

from .forms import EmailForm


def send_email_view(request):
    """
    Display the email form and send an email when the form is submitted.
    """

    if request.method == "POST":

        # Get submitted form data, including uploaded files
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():

            sender_email = form.cleaned_data["sender_email"]
            recipient_email = form.cleaned_data["recipient_email"]
            cc_emails = form.cleaned_data["cc_emails"]
            subject = form.cleaned_data["subject"]
            message_body = form.cleaned_data["message"]
            attachment = form.cleaned_data["attachment"]

            try:
                # Create the email
                email = EmailMessage(
                    subject=subject,
                    body=message_body,

                    # The SMTP account will be used as the actual sender.
                    # Reply-To allows the recipient to reply to the
                    # email address entered in the form.
                    from_email=None,

                    to=[recipient_email],
                    cc=cc_emails,
                    reply_to=[sender_email],
                )

                # Add attachment if the user selected a file
                if attachment:
                    email.attach(
                        attachment.name,
                        attachment.read(),
                        attachment.content_type,
                    )

                # Send the email through the configured SMTP server
                email.send(fail_silently=False)

                # Display success message
                messages.success(
                    request,
                    "Email sent successfully!"
                )

                # Create a fresh form after successful submission
                form = EmailForm()

            except Exception as e:
                # Display an error message if sending fails
                messages.error(
                    request,
                    f"Failed to send email: {str(e)}"
                )

    else:
        form = EmailForm()

    return render(
        request,
        "email_app/send_email.html",
        {"form": form}
    )