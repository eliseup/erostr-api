"""
Helpers for the shifts app.
"""
import uuid
import hashlib
from io import BytesIO

from typing import Tuple

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import ContentFile

from common.storages import MEDIA_PRIVATE_STORAGE


def generate_punch_file_code() -> str:
    return str(uuid.uuid4().hex[:6]).upper()


def persist_uploaded_punch_file(file: TemporaryUploadedFile) -> Tuple[str, str]:
    """
    Saves the given file into the MEDIA_PRIVATE_STORAGE folder.
    The file content is processed inside a for loop to permit sha256 hash calculations.
    """
    hasher = hashlib.sha256()
    file_buffer = BytesIO()

    file_name = f'{uuid.uuid4().hex}.csv'

    for chunk in file.chunks():
        hasher.update(chunk)
        file_buffer.write(chunk)

    MEDIA_PRIVATE_STORAGE.save(file_name, ContentFile(file_buffer.getvalue()))

    return file_name, hasher.hexdigest()
