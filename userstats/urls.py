from .views import IncomeSummaryStats
from django.urls import path


urlpatterns = [
    path('income-sources-data', IncomeSummaryStats.as_view(), name='income-sources-data'),
]
