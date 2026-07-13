from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Registration Successful!")
            return redirect("register")

    return render(request, "register.html")