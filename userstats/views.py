from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from rest_framework import status, response
from income.models import Income

# Create your views here.
class ExpenseSummaryStats(APIView):

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0

        for expense in expenses:
            amount += expense.amount

        return {'amount': str(amount)}

    def get_category(self, expense):
        return expense.category

    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30*12)
        expenses = Expense.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=today_date)

        final = {}

        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(expenses, category)

        return response.Response({'category_data': final}, status=status.HTTP_200_OK)


class IncomeSourcesSummaryStats(APIView):

    def get_amount_for_source(self, income_list, source):
        income = income_list.filter(source=source)
        amount = 0

        for i in income:
            amount += i.amount

        return {'amount': str(amount)}

    def get_source(self, income):
        return income.source

    def get(self, request):
        today_date = datetime.date.today()
        ayear_ago = today_date - datetime.timedelta(days=30*12)
        income = Income.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=today_date)

        final = {}

        sources = list(set(map(self.get_source, income)))

        for i in income:
            for source in sources:
                final[source] = self.get_amount_for_source(income, source)

        return response.Response({'income_source_data': final}, status=status.HTTP_200_OK)

