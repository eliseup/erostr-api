"""
Helpers for the shifts app.
"""
import uuid
import hashlib
import pandas as pd

from io import BytesIO

from typing import Tuple, Dict

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import ContentFile

from common.storages import MEDIA_PRIVATE_STORAGE
from shifts.models import TimePunch


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


def build_time_punch_graph_series(punch_date: str) -> Dict[str, int]:
    punches = (
        TimePunch.objects
        .filter(punch_date=punch_date)
        .order_by('employee_number', 'punch_date', 'punch_hour')
        .values('punch_date', 'punch_hour', 'employee_number')
    )

    df = pd.DataFrame(punches)

    # Create a new column datetime
    df['datetime'] = pd.to_datetime(
        df['punch_date'].astype(str) + ' ' + df['punch_hour'].astype(str)
    )

    grouped = df.groupby('employee_number')

    intervals = []

    for employee_number, group in grouped:
        times = group['datetime'].tolist()

        # Parts for employee (enter, exit)
        for i in range(0, len(times) - 1, 2):
            start = times[i]
            end = times[i + 1]
            intervals.append((start, end))

    # Create a time series with interval of 10 minutes.
    start_day = df['datetime'].min().replace(minute=0, second=0)
    end_day = df['datetime'].max().replace(minute=59, second=59)
    time_index = pd.date_range(start=start_day, end=end_day, freq='10min')

    # Start a new serie with zeros.
    presence_series = pd.Series(0, index=time_index)

    # Count how many are in each interval of time.
    for start, end in intervals:
        presence_series[(presence_series.index >= start) & (presence_series.index <= end)] += 1

    presence_series.index = presence_series.index.strftime('%H:%M')

    return presence_series.to_dict()
