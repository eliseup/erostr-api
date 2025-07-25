import pandas as pd

from celery import shared_task

from common.storages import MEDIA_PRIVATE_STORAGE
from shifts.models import TimePunchFile, TimePunch


@shared_task
def task_handle_uploaded_punch_file(
        uploaded_file_name: str,
        punch_file_id: int
) -> None:
    """
    This task processes a CSV punch file: parses rows, creates TimePunch records,
    and updates the TimePunchFile status.
    Reads and deletes the file from MEDIA_PRIVATE_STORAGE.
    """
    time_punch_file = TimePunchFile.objects.filter(id=punch_file_id).first()

    if time_punch_file and MEDIA_PRIVATE_STORAGE.exists(uploaded_file_name):
        valid_columns = ['matricula', 'data_marcacao', 'hora_marcacao']

        df = pd.read_csv(MEDIA_PRIVATE_STORAGE.path(uploaded_file_name), sep=';')
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        if not df.empty and df.columns.isin(valid_columns).all():
            total_rows = len(df)

            for row_number in range(total_rows):
                row = df.loc[row_number]

                TimePunch.objects.create(
                    time_punch_file=time_punch_file,
                    employee_number=row['matricula'],
                    punch_date = row['data_marcacao'],
                    punch_hour = row['hora_marcacao'],
                )

            time_punch_file.punch_count = total_rows
            time_punch_file.status = 'success'
            time_punch_file.save()

        else:
            time_punch_file.status = 'error'
            time_punch_file.save()

        MEDIA_PRIVATE_STORAGE.delete(uploaded_file_name)
