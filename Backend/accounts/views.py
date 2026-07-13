from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.http import HttpResponse
from reportlab.pdfgen import canvas

@login_required

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


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def resume_builder(request):

    if request.method == "POST":

        Resume.objects.create(
            user=request.user,
            full_name=request.POST["full_name"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            education=request.POST["education"],
            skills=request.POST["skills"]
        )

        return redirect("dashboard")

    return render(request, "resume.html")

@login_required
def view_resume(request):

    resume = Resume.objects.filter(user=request.user).first()

    return render(request, "resume_view.html", {
        "resume": resume
    })

@login_required
def download_resume(request):

    resume = Resume.objects.filter(user=request.user).first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, 800, "CareerPilot AI Resume")

    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Name: {resume.full_name}")
    p.drawString(50, 735, f"Phone: {resume.phone}")
    p.drawString(50, 710, f"Email: {resume.email}")
    p.drawString(50, 685, f"Education: {resume.education}")
    p.drawString(50, 660, "Skills:")
    p.drawString(70, 640, resume.skills)

    p.showPage()
    p.save()

    return response