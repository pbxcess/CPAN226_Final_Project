from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .validators import validate_attachment_list


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """A FileField that returns a validated list of uploaded files."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        files = data if isinstance(data, (list, tuple)) else [data]
        cleaned_files = [super(MultipleFileField, self).clean(item, initial) for item in files]
        return validate_attachment_list(cleaned_files)


class EmailForm(forms.Form):
    """
    Form used to collect the information required to send an email.

    The form collects the sender and recipient email addresses, optional
    CC recipients, the subject, message body, and an optional attachment.
    """

    sender_email = forms.EmailField(
        label="Sender Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "sender@example.com",
                "class": "form-control"
            }
        )
    )

    recipient_email = forms.EmailField(
        label="Recipient Email",
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
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write your message here...",
                "class": "form-control",
                "rows": 8
            }
        )
    )

    attachments = MultipleFileField(
        label="Attachments",
        required=False,
        help_text="Optional: up to 5 files, maximum 5 MB each.",
        widget=MultipleFileInput(
            attrs={
                "class": "form-control",
                "multiple": True,
            }
        )
    )

    def clean_sender_email(self):
        return self.cleaned_data["sender_email"].strip().lower()

    def clean_recipient_email(self):
        return self.cleaned_data["recipient_email"].strip().lower()

    def clean_cc_emails(self):
        raw_value = self.cleaned_data.get("cc_emails", "")
        normalized_value = raw_value.replace(";", ",").replace("\n", ",")
        addresses = [address.strip().lower() for address in normalized_value.split(",") if address.strip()]

        invalid_addresses = []
        for address in addresses:
            try:
                validate_email(address)
            except ValidationError:
                invalid_addresses.append(address)

        if invalid_addresses:
            raise ValidationError("Invalid CC address(es): " + ", ".join(invalid_addresses))
        return addresses

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()
        if not subject:
            raise ValidationError("Subject is required.")
        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if not message:
            raise ValidationError("Message is required.")
        return message
