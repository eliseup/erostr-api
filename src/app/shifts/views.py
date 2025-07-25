from django.core.files.uploadedfile import TemporaryUploadedFile

from rest_framework import generics
from rest_framework.exceptions import UnsupportedMediaType, ValidationError
from rest_framework.parsers import MultiPartParser

from shifts.helpers import generate_punch_file_code, persist_uploaded_punch_file
from shifts.models import TimePunch, TimePunchFile
from shifts.serializers import TimePunchSerializer, TimePunchFileSerializer
from shifts.tasks import task_handle_uploaded_punch_file


class TimePunchFileListCreateView(generics.ListCreateAPIView):
    queryset = TimePunchFile.objects.all()
    serializer_class = TimePunchFileSerializer
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        """
        Handles the creation of a TimePunchFile instance from an uploaded CSV file.

        This method performs the following steps:
        - Validates that a file was included in the request.
        - Verifies that the uploaded file is of type 'text/csv'.
        - Persists the uploaded file to storage and calculates its fingerprint.
        - Checks if a file with the same fingerprint already exists to avoid duplicates.
        - Saves the new TimePunchFile instance with metadata (name, code, fingerprint).

        Raises:
        ValidationError: If no file is provided or if a duplicate file is detected.
        UnsupportedMediaType: If the uploaded file is not a valid CSV.
        """
        valid_content_type = 'text/csv'

        file: TemporaryUploadedFile = self.request.data.get('file')

        if file:
            if file.content_type != valid_content_type:
                raise UnsupportedMediaType(
                    media_type=file.content_type,
                    detail=f'Expected {valid_content_type}, got {file.content_type} instead.'
                )

            saved_file_name, file_hash = persist_uploaded_punch_file(file=file)

            if TimePunchFile.objects.filter(fingerprint=file_hash).exists():
                raise ValidationError(detail=f'File {file.name} already exists.')

            record = serializer.save(
                name=file.name,
                code=generate_punch_file_code(),
                fingerprint=file_hash,
            )

            task_handle_uploaded_punch_file.delay(
                uploaded_file_name=saved_file_name,
                punch_file_id=record.pk
            )

        else:
            raise ValidationError(detail='No file provided.')


class TimePunchListView(generics.ListAPIView):
    queryset = TimePunch.objects.all()
    serializer_class = TimePunchSerializer
