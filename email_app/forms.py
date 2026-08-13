from django import forms


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

    attachment = forms.FileField(
        label="Attachment",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control"
            }
        )
    )