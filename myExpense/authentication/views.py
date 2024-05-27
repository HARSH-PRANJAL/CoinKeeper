import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# external packages
from validate_email import validate_email


# Create your views here.
class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):

        # get user data
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        context = {"fieldValues": request.POST}

        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request, "Password should be 8 charecter long")
                    return render(request, "authentication/register.html", context)

                # new user creation process
                try:
                    # adding user to data base
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    transaction.commit()
                    messages.success(request, "Account created")
                except Exception as e:
                    messages.error(request, f"Server - Database error {str(e)}")
                    transaction.rollback()
            else:
                messages.error(request, "Email already exists")
                return render(request, "authentication/register.html", context)

        else:
            messages.error(request, "User name already exists")
            return render(request, "authentication/register.html", context)

        return redirect("login")


class UservalidationView(View):
    def post(self, request):
        # json.load convert inputs into a dict
        # resuest.body contains the data from frontend
        messages.get_messages(request)
        data = json.loads(request.body)

        username = data["username"]
        print(username)

        if not str(username).isalnum():
            # this is how django sends json data to frontend
            # json is always in a dict format and key is always a string
            return JsonResponse(
                {"error": "username should be alphanumeric"}, status=400
            )

        if User.objects.filter(username=str(username)).exists():
            return JsonResponse({"error": "username is already taken"}, status=409)

        return JsonResponse({"username": True})


class EmailvalidationView(View):
    def post(self, request):
        # json.load convert inputs into a dict
        # request.body contains the data from frontend
        messages.get_messages(request)
        data = json.loads(request.body)

        email = data["email"]
        print(email)

        if not validate_email(email):
            # this is how django sends json data to frontend
            # json is always in a dict format and key is always a string
            return JsonResponse({"error": "not a valid email"}, status=400)

        if User.objects.filter(email=str(email)).exists():
            return JsonResponse({"error": "email in use"}, status=409)

        return JsonResponse({"email_valid": True})


class UserLoginView(View):
    def get(self, request):
        msg = request.GET.get("message")
        if msg:
            messages.warning(request, msg)
        return render(request, "authentication/login.html")

    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Logged in successfully.")
                    return redirect("expenses")
                else:
                    messages.error(request, "Your account is not active.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please provide both username and password.")

        return redirect("login")


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successfully.")
        return redirect("login")


class UserResetPassword(View):
    def get(self, request):
        return render(request, "authentication/resetPassword.html")

    def post(self, request):
        data = request.POST
        context = {"fieldValues": request.POST}
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        if len(password1) < 8:
            messages.error(request, "Password should be 8 charecter long")
            return render(request, "authentication/resetPassword.html", context)

        user = User.objects.filter(email=email)
        if user.exists():
            if not User.objects.filter(username=username).exists():
                messages.error(request, "This username dose not exists")
                return render(request, "authentication/resetPassword.html", context)
            else:
                if password1 == password2:
                    user = User.objects.get(email=email)
                    user.set_password(password1)
                    user.save()
                    messages.success(request, "Password reset successfull")
                    return redirect("login")
                else:
                    messages.error(request, "Passwords don't match")
                    return render(request, "authentication/resetPassword.html", context)
        else:
            messages.error(request, "This email dose not exists")
            return render(request, "authentication/resetPassword.html", context)
