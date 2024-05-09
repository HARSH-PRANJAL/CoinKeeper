from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now,null=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return (str(self.owner) +" " + str(self.category))

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
