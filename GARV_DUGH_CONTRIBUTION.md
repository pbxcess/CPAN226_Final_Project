# Garv Dugh (N01763558) - Completed Project Parts

## Responsibilities completed

- Implemented safe handling for multiple file attachments.
- Added a maximum of five files and a 5 MB limit per file.
- Blocked common executable and script file types.
- Sanitized filenames before passing attachments to the email back end.
- Added validation for sender, recipient, multiple CC addresses, subject, and message.
- Normalized email addresses and removed extra spaces.
- Displayed field-specific validation messages in the user interface.
- Added automated tests for valid and invalid inputs and attachments.
- Added comments explaining the handoff to the SMTP back-end work.

## Test command

Run from the project folder:

```powershell
python manage.py test email_app
```

## Expected result

All 11 tests should pass.

## Screenshots for the final report

1. The completed email form with the multiple attachment control.
2. A valid form submission with sender, recipient, CC, subject, and message.
3. The error displayed for an invalid CC email address.
4. The error displayed for a blocked `.exe` attachment.
5. The error displayed for an attachment larger than 5 MB.
6. The terminal showing all 11 tests passing.

## Back-end handoff

After the form is valid, `form.cleaned_data["attachments"]` contains a list of safe, validated uploaded files. The group member responsible for SMTP can loop over this list and attach each file to Django's `EmailMessage` object.
