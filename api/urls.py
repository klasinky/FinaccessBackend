from django.urls import path
from api.views.categories import list_category
from api.views.entries import EntryCreateView, EntryViewSet, EntryUploadXLS, EntryDownloadXLS
from api.views.expenses import ExpenseCreateView, ExpenseViewSet, ExpenseUploadXLS, ExpenseDownloadXLS
from api.views.months import MonthViewSet

# Month

month_create = MonthViewSet.as_view({
    'post': 'create'
})

month_list = MonthViewSet.as_view({
    'get': 'list',
})

month_viewset = MonthViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

category_expense_stats = MonthViewSet.as_view({
    'get': 'category_expenses_stats'
})

category_entry_stats = MonthViewSet.as_view({
    'get': 'category_entries_stats'
})

# Expense

expense_create = ExpenseCreateView.as_view({
    'post': 'create'
})

expense_viewset = ExpenseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Entry
entry_create = EntryCreateView.as_view({
    'post': 'create'
})

entry_viewset = EntryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Months
    path('months', month_create, name="months"),
    path('months/all', month_list, name="months-list"),
    path('months/<int:id>', month_viewset, name='months-viewset'),
    path('months/<int:id>/category/stats/expense', category_expense_stats, name='months-stats-category-expense'),
    path('months/<int:id>/category/stats/entry', category_entry_stats, name='months-stats-category-entry'),

    # Category
    path('categories/all', list_category.as_view(), name="category-all"),

    # Expense
    path('months/<int:id>/create/expense', expense_create, name="expenses"),
    path('expenses/<int:id>', expense_viewset, name="expenses-viewset"),

    # Entry
    path('months/<int:id>/create/entry', entry_create, name="entries"),
    path('entries/<int:id>', entry_viewset, name="entries-viewset"),

    # Import XLSX
    path('months/<int:id>/import/expense', ExpenseUploadXLS.as_view(), name="expenses-upload-xls"),
    path('months/<int:id>/import/entry', EntryUploadXLS.as_view(), name="entries-upload-xls"),

    # Export XLSX
    path('months/<int:id>/export/expense', ExpenseDownloadXLS.as_view(), name="expenses-download-xls"),
    path('months/<int:id>/export/entry', EntryDownloadXLS.as_view(), name="entries-download-xls")
]
