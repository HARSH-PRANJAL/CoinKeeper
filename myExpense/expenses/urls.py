from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="expenses"),
    path("addExpenses", views.addExpenses, name="addExpenses"),
    path("deleteExpense", views.deleteExpense, name="deleteExpense"),
    path("updateExpense", views.updateExpense, name="updateExpense"),
    path("searchExpense", csrf_exempt(views.searchExpense), name="searchExpense"),
    path("expenseSummary", views.expenseSummary, name="expenseSummary"),
    path("viewSummary", views.viewSummary, name="viewSummary"),
]
