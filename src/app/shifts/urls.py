from django.urls import path

from shifts.views import TimePunchFileListCreateView, TimePunchListView


urlpatterns = [
    path('shifts', TimePunchFileListCreateView.as_view(), name='time_punch_file_list_create'),
    path('shifts/punches', TimePunchListView.as_view(), name='time_punch_list'),
]