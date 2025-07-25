from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Custom Django file storage used for saving private media files.
MEDIA_PRIVATE_STORAGE = FileSystemStorage(
    location=settings.MEDIA_PRIVATE,
    file_permissions_mode=0o664,
    directory_permissions_mode=0o775
)
