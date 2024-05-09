from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.index, name="income"),
    path("addIncomes", views.addIncomes, name="addIncomes"),
    path("deleteIncome", views.deleteIncome, name="deleteIncome"),
    path("updateIncome", views.updateIncome, name="updateIncome"),
    path("searchIncome", csrf_exempt(views.searchIncome), name="searchIncome"),
]
