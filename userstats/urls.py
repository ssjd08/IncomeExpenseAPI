from django.urls import path
from .views import ExpenseSummaryStats


urlpatterns = [
    path ('expense_gategory_data', ExpenseSummaryStats.as_view(), name='expense_gategory_data')
]
