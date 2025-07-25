from django.urls import path

from shifts.views import TimePunchFileListCreateView, TimePunchListView, \
    TimePunchGraphSeriesRetrieveView


urlpatterns = [
    path('shifts', TimePunchFileListCreateView.as_view(), name='time_punch_file_list_create'),
    path('shifts/punches', TimePunchListView.as_view(), name='time_punch_list'),
    path(
        'shifts/punches/graph-series',
        TimePunchGraphSeriesRetrieveView.as_view(),
        name='time_punches_graph_series'
    ),
]