from django.shortcuts import redirect, render
from django.contrib import messages
from .models import UserPrefernces
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os, json


# Create your views here.
@login_required(login_url="authentication/userlogin")
def index(request):

    curency_data = []
    file_path = os.path.join("currencies.json")

    with open(file_path, "r") as file:
        data = json.load(file)
        for k, v in data.items():
            curency_data.append({"name": k, "value": v})

    exists = UserPrefernces.objects.filter(user=request.user).exists()
    user_prefrences = None
    if exists:
        user_prefrences = UserPrefernces.objects.get(user=request.user)

    if request.method == "GET":
        # for debugging
        # import pdb
        # pdb.set_trace()
        return render(
            request,
            "preferences/index.html",
            {"curency_data": curency_data, "user_prefrences": user_prefrences},
        )
    else:
        curency = request.POST["curency"]
        if exists:
            user_prefrences.currency = curency
            user_prefrences.save()
            messages.success(request, "Settings Saved")
        else:
            UserPrefernces.objects.create(user=request.user, currency=curency)
            messages.success(request, "Settings Saved")
        return render(
            request,
            "preferences/index.html",
            {"curency_data": curency_data, "user_prefrences": user_prefrences},
        )
