import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPrefernces
import json
import re


# Create your views here.
@login_required(login_url="authentication/userlogin")
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    curency = UserPrefernces.objects.filter(user=request.user)
    if curency:
        curency = UserPrefernces.objects.get(user=request.user).currency
    else:
        curency = None
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)

    if curency:
        pattern = re.search(r"^[^-]*", curency)
        curency = pattern.group()

    return render(
        request,
        "expenses/index.html",
        {"expenses": expenses, "page_obj": page_obj, "curency": curency},
    )


@login_required(login_url="authentication/userlogin")
def addExpenses(request):
    existingCategory = Category.objects.all()
    values = request.POST
    viewName = "addExpenses"

    if request.method == "POST":
        data = request.POST
        amount = data.get("amount")
        if not amount:
            messages.warning(request, "Amount required")
        else:
            description = data.get("description")
            category = data.get("category")
            date = data.get("date")
            owner = request.user
            newExpense = None
            if category:
                if date:
                    newExpense = Expense.objects.create(
                        amount=amount,
                        owner=owner,
                        date=date,
                        category=category,
                        description=description,
                    )
                else:
                    newExpense = Expense.objects.create(
                        amount=amount,
                        owner=owner,
                        category=category,
                        description=description,
                    )
                messages.success(request, "Values inserted")
                newExpense.save()
                return redirect("expenses")
            else:
                messages.warning(request, "Category is required")

    return render(
        request,
        "expenses/addExpenses.html",
        {"categories": existingCategory, "values": values, "viewName": viewName},
    )


@login_required(login_url="authentication/userlogin")
def deleteExpense(request):
    if request.method == "POST":
        op = request.POST
        pk = op.get("delete")
        expense = Expense.objects.get(id=pk)
        expense.delete()

    return redirect("expenses")


@login_required(login_url="authentication/userlogin")
def updateExpense(request):
    viewname = "updateExpense"
    existingCategory = Category.objects.all()
    if request.method == "GET":
        op = request.GET
        pk = op.get("update")
        expense = Expense.objects.get(id=pk)
        return render(
            request,
            "expenses/addExpenses.html",
            {"categories": existingCategory, "values": expense, "viewName": viewname},
        )
    else:
        if request.method == "POST":
            data = request.POST
            pk = data.get("update")
            expense = Expense.objects.get(id=pk)
            amount = data.get("amount")
            if not amount:
                messages.warning(request, "Amount required")
                return render(
                    request,
                    "expenses/addExpenses.html",
                    {
                        "categories": existingCategory,
                        "values": expense,
                        "viewName": viewname,
                    },
                )
            else:
                description = data.get("description")
                category = data.get("category")
                date = data.get("date")
                if category:
                    if not date:
                        expense.amount = amount
                        expense.description = description
                        expense.category = category
                    else:
                        expense.amount = amount
                        expense.description = description
                        expense.category = category
                        expense.date = date

                    messages.success(request, "Values updates")
                    expense.save()
                    return redirect("expenses")
                else:
                    messages.warning(request, "Category is required")
                    return render(
                        request,
                        "expenses/addExpenses.html",
                        {
                            "categories": existingCategory,
                            "values": expense,
                            "viewName": viewname,
                        },
                    )

        return redirect("expenses")


def searchExpense(request):

    if request.method == "POST":
        searchStr = json.loads(request.body).get("search")
        expenses = (
            Expense.objects.filter(amount__istartswith=searchStr, owner=request.user)
            | Expense.objects.filter(date__istartswith=searchStr, owner=request.user)
            | Expense.objects.filter(category__icontains=searchStr, owner=request.user)
            | Expense.objects.filter(
                description__icontains=searchStr, owner=request.user
            )
        )

        data = expenses.values()
        return JsonResponse(list(data), safe=False)


def expenseSummary(request):
    today_date = datetime.date.today()
    sixMonths = today_date - datetime.timedelta(days=30 * 6)
    expenses = Expense.objects.filter(
        owner=request.user, date__gte=sixMonths, date__lte=today_date
    )

    # categories = list({i.category for i in expenses})
    finalExpense = {}

    for data in expenses:
        if data.category not in finalExpense:
            finalExpense[data.category] = data.amount
        else:
            finalExpense[data.category] += data.amount

    return JsonResponse({"expenseSummaryData": finalExpense}, safe=False)

def viewSummary(request):
    return render(request,"expenses/summary.html")
    
