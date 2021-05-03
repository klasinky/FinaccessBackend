from django.urls import path
from api.views.categories import CategoryAPIView
from api.views.comments import CommentCreateView, CommentDestroyView, CommentListView, CommentLikeView
from api.views.companystock import CompanyStockListView, CompanyStockView, CompanyListView
from api.views.currency import CurrencyAPIView
from api.views.entries import EntryCreateView, EntryViewSet, EntryUploadXLS, EntryDownloadXLS
from api.views.expenses import ExpenseCreateView, ExpenseViewSet, ExpenseUploadXLS, ExpenseDownloadXLS
from api.views.months import MonthViewSet
from api.views.posts import PostViewSet, PostLikeView

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

list_amount_month = MonthViewSet.as_view({
    'get': 'get_amount_base_all'
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

# Post

post_viewset = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

post_create_list = PostViewSet.as_view({
    'post': 'create',
    'get': 'list'
})


post_change_finished = PostViewSet.as_view({
    'patch': 'change_finished_post'
})

# Comment



urlpatterns = [
    # Months
    path('months', month_create, name="months"),
    path('months/all', month_list, name="months-list"),
    path('months/<int:id>', month_viewset, name='months-viewset'),
    path('months/<int:id>/amounts', list_amount_month, name='months-amount-list'),
    path('months/<int:id>/category/stats/expense', category_expense_stats, name='months-stats-category-expense'),
    path('months/<int:id>/category/stats/entry', category_entry_stats, name='months-stats-category-entry'),

    # Category
    path('categories/all', CategoryAPIView.as_view(), name="category-all"),

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
    path('months/<int:id>/export/entry', EntryDownloadXLS.as_view(), name="entries-download-xls"),

    # Post
    path('posts', post_create_list, name="posts-create-list"),
    path('posts/<int:id>', post_viewset, name="posts-viewset"),
    path('posts/<int:id>/finished', post_change_finished, name="posts-change-finished"),
    path('posts/<int:id>/like', PostLikeView.as_view(), name="posts-like"),

    # Comment
    path('posts/<int:idpost>/comment', CommentCreateView.as_view({'post': 'create'}), name="comments-create"),
    path('posts/<int:idpost>/<int:idparent>/comment', CommentCreateView.as_view({'post': 'create'}), name="comments-create"),
    path('comment/<int:id>/delete', CommentDestroyView.as_view({'delete': 'destroy'}), name="comments-delete"),
    path('posts/<int:idpost>/comment/all', CommentListView.as_view({'get': 'list'}), name="comments-list"),
    path('comment/<int:id>/like', CommentLikeView.as_view(), name="comments-like"),

    # CompanyStockView
    path('stocks/<int:id>', CompanyStockView.as_view(), name="companystock-view"),
    path('stocks', CompanyStockListView.as_view(), name="companystock-list"),
    path('stocks/all', CompanyListView.as_view(), name="companystock-all"),

    # Currency
    path('currencies', CurrencyAPIView.as_view(), name="currency")
]
