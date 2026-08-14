from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from .forms import EmailForm


VALID_DATA = {
    "sender_email": "Sender@Example.com",
    "recipient_email": "Recipient@Example.com",
    "cc_emails": "one@example.com; TWO@example.com",
    "subject": "CPAN226 Project Test",
    "message": "Testing validation and attachments.",
}


class EmailFormTests(SimpleTestCase):
    def test_valid_form_normalizes_email_addresses(self):
        form = EmailForm(VALID_DATA)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["sender_email"], "sender@example.com")
        self.assertEqual(form.cleaned_data["recipient_email"], "recipient@example.com")
        self.assertEqual(form.cleaned_data["cc_emails"], ["one@example.com", "two@example.com"])

    def test_invalid_sender_is_rejected(self):
        form = EmailForm({**VALID_DATA, "sender_email": "wrong"})
        self.assertFalse(form.is_valid())
        self.assertIn("sender_email", form.errors)

    def test_invalid_recipient_is_rejected(self):
        form = EmailForm({**VALID_DATA, "recipient_email": "wrong"})
        self.assertFalse(form.is_valid())
        self.assertIn("recipient_email", form.errors)

    def test_invalid_cc_is_rejected(self):
        form = EmailForm({**VALID_DATA, "cc_emails": "good@example.com, wrong"})
        self.assertFalse(form.is_valid())
        self.assertIn("cc_emails", form.errors)

    def test_blank_subject_is_rejected(self):
        form = EmailForm({**VALID_DATA, "subject": "   "})
        self.assertFalse(form.is_valid())

    def test_blank_message_is_rejected(self):
        form = EmailForm({**VALID_DATA, "message": "   "})
        self.assertFalse(form.is_valid())

    def test_safe_attachment_is_accepted(self):
        file = SimpleUploadedFile("notes.txt", b"Network programming")
        form = EmailForm(VALID_DATA, {"attachments": file})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["attachments"][0].name, "notes.txt")

    def test_executable_attachment_is_rejected(self):
        file = SimpleUploadedFile("program.exe", b"blocked")
        form = EmailForm(VALID_DATA, {"attachments": file})
        self.assertFalse(form.is_valid())
        self.assertIn("attachments", form.errors)

    def test_oversized_attachment_is_rejected(self):
        file = SimpleUploadedFile("large.txt", b"x" * (5 * 1024 * 1024 + 1))
        form = EmailForm(VALID_DATA, {"attachments": file})
        self.assertFalse(form.is_valid())
        self.assertIn("attachments", form.errors)

    def test_empty_attachment_is_rejected(self):
        file = SimpleUploadedFile("empty.txt", b"")
        form = EmailForm(VALID_DATA, {"attachments": file})
        self.assertFalse(form.is_valid())
        self.assertIn("attachments", form.errors)

    def test_more_than_five_attachments_are_rejected(self):
        files = [SimpleUploadedFile(f"file{i}.txt", b"ok") for i in range(6)]
        form = EmailForm(VALID_DATA, {"attachments": files})
        self.assertFalse(form.is_valid())
        self.assertIn("attachments", form.errors)

# Create your tests here.
