from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class EmailForm(forms.Form):
    """
    Form used to collect the information required to send an email.

    The form collects the sender and recipient email addresses, optional
    CC recipients, the subject, message body, and an optional attachment.
    """

    sender_email = forms.EmailField(
        label="Sender Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "sender@example.com",
                "class": "form-control"
            }
        )
    )

    recipient_email = forms.EmailField(
        label="Recipient Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "recipient@example.com",
                "class": "form-control"
            }
        )
    )

    cc_emails = forms.CharField(
        label="CC",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "email1@example.com, email2@example.com",
                "class": "form-control"
            }
        )
    )

    subject = forms.CharField(
        label="Subject",
        required=True,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter email subject",
                "class": "form-control"
            }
        )
    )

    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write your message here...",
                "class": "form-control",
                "rows": 8
            }
        )
    )

    attachment = forms.FileField(
        label="Attachment",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    def clean_cc_emails(self):
        """
        Validate multiple CC email addresses.

        Users can enter multiple email addresses separated by
        commas or semicolons.
        """

        cc_value = self.cleaned_data.get("cc_emails", "").strip()

        # CC is optional
        if not cc_value:
            return []

        # Allow both comma and semicolon separators
        cc_value = cc_value.replace(";", ",")

        emails = [
            email.strip()
            for email in cc_value.split(",")
            if email.strip()
        ]

        invalid_emails = []

        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            raise forms.ValidationError(
                "Invalid CC email address(es): "
                + ", ".join(invalid_emails)
            )

        return emails

    def clean_attachment(self):
        """
        Validate the uploaded attachment.

        Maximum attachment size is 10 MB.
        """

        attachment = self.cleaned_data.get("attachment")

        if attachment:
            max_size = 10 * 1024 * 1024  # 10 MB

            if attachment.size > max_size:
                raise forms.ValidationError(
                    "Attachment size cannot exceed 10 MB."
                )

        return attachment