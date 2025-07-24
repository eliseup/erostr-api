from rest_framework import generics

from shifts.models import TimePunch, TimePunchFile
from shifts.serializers import TimePunchSerializer, TimePunchFileSerializer


class TimePunchFileListCreateView(generics.ListCreateAPIView):
    queryset = TimePunchFile.objects.all()
    serializer_class = TimePunchFileSerializer


class TimePunchListView(generics.ListAPIView):
    queryset = TimePunch.objects.all()
    serializer_class = TimePunchSerializer
