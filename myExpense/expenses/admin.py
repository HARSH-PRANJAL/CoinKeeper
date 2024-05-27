from django.contrib import admin
from .models import Expense, Category

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    # these are predefined tuple names don't chage it
    list_display = (
        "amount",
        "owner",
        "category",
        "description",
        "date",
    )
    search_fields = (
        "category",
        "description",
        "date",
    )
    # to add pagination to search result
    list_per_page = 5


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
