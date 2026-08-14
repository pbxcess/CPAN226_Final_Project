from pathlib import Path

from django.core.exceptions import ValidationError
from django.utils.text import get_valid_filename


MAX_ATTACHMENT_COUNT = 5
MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024
BLOCKED_EXTENSIONS = {
    ".bat", ".cmd", ".com", ".exe", ".jar", ".js",
    ".msi", ".ps1", ".scr", ".sh", ".vbs",
}


def validate_attachment(uploaded_file):
    """Reject empty, oversized, unsafe, or unnamed attachments."""
    original_name = Path(uploaded_file.name or "").name
    extension = Path(original_name).suffix.lower()

    if not original_name:
        raise ValidationError("Each attachment must have a filename.")
    if uploaded_file.size == 0:
        raise ValidationError(f"{original_name} is empty.")
    if uploaded_file.size > MAX_ATTACHMENT_SIZE:
        raise ValidationError(f"{original_name} must be 5 MB or smaller.")
    if extension in BLOCKED_EXTENSIONS:
        raise ValidationError(f"The file type {extension} is not allowed.")

    # Remove path characters and unsafe filename characters before the file is
    # passed to the email back end.
    uploaded_file.name = get_valid_filename(original_name)
    return uploaded_file


def validate_attachment_list(uploaded_files):
    """Validate all uploaded attachments and enforce the file-count limit."""
    files = list(uploaded_files or [])
    if len(files) > MAX_ATTACHMENT_COUNT:
        raise ValidationError("You can attach a maximum of 5 files.")
    return [validate_attachment(uploaded_file) for uploaded_file in files]
