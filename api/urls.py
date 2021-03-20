from django.urls import path

from api.views.months import MonthViewSet

month_create = MonthViewSet.as_view({
    'post': 'create'
})

month_list = MonthViewSet.as_view({
    'get': 'list',
})

month_retrieve_update = MonthViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})

month_delete = MonthViewSet.as_view({
    'delete': 'destroy'
})

urlpatterns = [
    path('months', month_create, name="months"),
    path('months/all', month_list, name="months-list"),
    path('months/<int:id>', month_retrieve_update, name='months-retrieve-update'),
    path('months/<int:id>/delete', month_delete, name='months-delete'),
]
