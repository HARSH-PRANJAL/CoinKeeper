from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json


# Create your views here.
@login_required(login_url="authentication/userlogin")
def index(request):
    Incomes = Income.objects.filter(owner=request.user)
    if Incomes:
        paginator = Paginator(Incomes, 4)
        page_number = request.GET.get("page")
        page_obj = Paginator.get_page(paginator, page_number)
        return render(
            request, "income/index.html", {"Incomes": Incomes, "page_obj": page_obj}
        )
    return render(
        request,
        "income/index.html",
    )


@login_required(login_url="authentication/userlogin")
def addIncomes(request):
    existingSource = Source.objects.all()
    values = request.POST
    viewName = "addIncomes"

    if request.method == "POST":
        data = request.POST
        amount = data.get("amount")
        if not amount:
            messages.warning(request, "Amount required")
        else:
            description = data.get("description")
            source = data.get("ource")
            date = data.get("date")
            owner = request.user
            newIncome = None
            if Source:
                if date:
                    newIncome = Income.objects.create(
                        amount=amount,
                        owner=owner,
                        date=date,
                        source=source,
                        description=description,
                    )
                else:
                    newIncome = Income.objects.create(
                        amount=amount,
                        owner=owner,
                        source=source,
                        description=description,
                    )
                messages.success(request, "Values inserted")
                newIncome.save()
                return redirect("Incomes")
            else:
                messages.warning(request, "Source is required")

    return render(
        request,
        "incomes/addIncomes.html",
        {"categories": existingSource, "values": values, "viewName": viewName},
    )


@login_required(login_url="authentication/userlogin")
def deleteIncome(request):
    if request.method == "POST":
        op = request.POST
        pk = op.get("delete")
        expense = Income.objects.get(id=pk)
        expense.delete()

    return redirect("expenses")


@login_required(login_url="authentication/userlogin")
def updateIncome(request):
    viewname = "updateIncome"
    existingCategory = Category.objects.all()
    if request.method == "GET":
        op = request.GET
        pk = op.get("update")
        expense = Income.objects.get(id=pk)
        return render(
            request,
            "expenses/addIncomes.html",
            {"categories": existingCategory, "values": expense, "viewName": viewname},
        )
    else:
        if request.method == "POST":
            data = request.POST
            pk = data.get("update")
            expense = Income.objects.get(id=pk)
            amount = data.get("amount")
            if not amount:
                messages.warning(request, "Amount required")
                return render(
                    request,
                    "expenses/addIncomes.html",
                    {
                        "categories": existingCategory,
                        "values": expense,
                        "viewName": viewname,
                    },
                )
            else:
                description = data.get("description")
                source = data.get("source")
                date = data.get("date")
                if source:
                    if not date:
                        expense.amount = amount
                        expense.description = description
                        expense.source = source
                    else:
                        expense.amount = amount
                        expense.description = description
                        expense.source = source
                        expense.date = date

                    messages.success(request, "Values updates")
                    expense.save()
                    return redirect("expenses")
                else:
                    messages.warning(request, "Category is required")
                    return render(
                        request,
                        "expenses/addIncomes.html",
                        {
                            "categories": existingCategory,
                            "values": expense,
                            "viewName": viewname,
                        },
                    )

        return redirect("expenses")


def searchIncome(request):

    if request.method == "POST":
        searchStr = json.loads(request.body).get("search")
        expenses = (
            Income.objects.filter(amount__istartswith=searchStr, owner=request.user)
            | Income.objects.filter(date__istartswith=searchStr, owner=request.user)
            | Income.objects.filter(source__icontains=searchStr, owner=request.user)
            | Income.objects.filter(
                description__icontains=searchStr, owner=request.user
            )
        )

        data = expenses.values()
        return JsonResponse(list(data), safe=False)
