from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import generics
from rest_framework.exceptions import UnsupportedMediaType, ValidationError, NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from shifts.helpers import generate_punch_file_code, persist_uploaded_punch_file
from shifts.models import TimePunch, TimePunchFile
from shifts.serializers import TimePunchSerializer, TimePunchFileSerializer, \
    TimePunchGraphSeriesSerializer
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
    filterset_fields = ['employee_number']


class TimePunchGraphSeriesRetrieveView(generics.RetrieveAPIView):
    serializer_class = TimePunchSerializer

    def get(self, request, *args, **kwargs):
        punch_date = self.request.query_params.get('punch_date')

        if punch_date is not None:
            try:
                TimePunch.objects.filter(punch_date=punch_date).exists()
            except DjangoValidationError:
                raise NotFound(detail='Nothing was found.')

            serializer = TimePunchGraphSeriesSerializer(
                data={},
                context={'punch_date': punch_date}
            )

            serializer.is_valid()

            return Response(serializer.data)

        raise NotFound(detail='Nothing was found.')
