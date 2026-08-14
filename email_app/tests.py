from unittest.mock import patch

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .forms import EmailForm


class EmailFormTests(TestCase):
    """
    Tests for email form validation.
    """

    def test_valid_form(self):
        """
        The form should be valid when all required information is correct.
        """
        form = EmailForm(
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "cc1@example.com, cc2@example.com",
                "subject": "Test Subject",
                "message": "This is a test message.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_sender_email(self):
        """
        The form should reject an invalid sender email.
        """
        form = EmailForm(
            data={
                "sender_email": "invalid-email",
                "recipient_email": "recipient@example.com",
                "subject": "Test Subject",
                "message": "Test message",
            }
        )

        self.assertFalse(form.is_valid())

    def test_invalid_recipient_email(self):
        """
        The form should reject an invalid recipient email.
        """
        form = EmailForm(
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "invalid-email",
                "subject": "Test Subject",
                "message": "Test message",
            }
        )

        self.assertFalse(form.is_valid())

    def test_multiple_cc_emails(self):
        """
        Multiple CC email addresses should be accepted.
        """
        form = EmailForm(
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "cc1@example.com, cc2@example.com",
                "subject": "Test Subject",
                "message": "Test message",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["cc_emails"],
            ["cc1@example.com", "cc2@example.com"],
        )

    def test_invalid_cc_email(self):
        """
        Invalid CC addresses should be rejected.
        """
        form = EmailForm(
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "cc1@example.com, invalid-email",
                "subject": "Test Subject",
                "message": "Test message",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cc_emails", form.errors)

    def test_empty_cc_is_allowed(self):
        """
        CC is optional.
        """
        form = EmailForm(
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "",
                "subject": "Test Subject",
                "message": "Test message",
            }
        )

        self.assertTrue(form.is_valid())


class EmailSendingTests(TestCase):
    """
    Tests for email sending functionality.
    """

    @patch("email_app.views.EmailMessage.send")
    def test_email_is_sent(self, mock_send):
        """
        The email should be sent when valid form data is submitted.
        """
        mock_send.return_value = 1

        response = self.client.post(
            "/",
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "cc1@example.com, cc2@example.com",
                "subject": "Test Subject",
                "message": "This is a test message.",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()

    @patch("email_app.views.EmailMessage.send")
    def test_email_with_attachment(self, mock_send):
        """
        The email should support file attachments.
        """
        mock_send.return_value = 1

        uploaded_file = SimpleUploadedFile(
            "test.txt",
            b"This is a test attachment.",
            content_type="text/plain",
        )

        response = self.client.post(
            "/",
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "cc@example.com",
                "subject": "Test with Attachment",
                "message": "This email contains an attachment.",
                "attachment": uploaded_file,
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()

    @patch("email_app.views.EmailMessage.send")
    def test_email_without_cc(self, mock_send):
        """
        The email should be sent when CC is empty.
        """
        mock_send.return_value = 1

        response = self.client.post(
            "/",
            data={
                "sender_email": "sender@example.com",
                "recipient_email": "recipient@example.com",
                "cc_emails": "",
                "subject": "No CC Test",
                "message": "This email has no CC recipients.",
            },
        )

        self.assertEqual(response.status_code, 200)
        mock_send.assert_called_once()