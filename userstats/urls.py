from .views import IncomeSummaryStats, ExpenseSummaryStats
from django.urls import path


urlpatterns = [
    path('income-sources-data', IncomeSummaryStats.as_view(), name='income-sources-data'),
    path ('expense_gategory_data', ExpenseSummaryStats.as_view(), name='expense_gategory_data'),
]
