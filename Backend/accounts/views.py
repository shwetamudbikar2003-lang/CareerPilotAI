from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .forms import ResumeForm
from .gemini import generate_interview_questions
from .gemini import client
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
@login_required
def resume_builder(request):

    resume = Resume.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = ResumeForm(request.POST, instance=resume)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect("view_resume")

    else:
        form = ResumeForm(instance=resume)

    return render(request, "resume.html", {
        "form": form
    })


@login_required
def edit_resume(request):

    resume = Resume.objects.filter(user=request.user).first()

    if request.method == "POST":

        resume.full_name = request.POST["full_name"]
        resume.phone = request.POST["phone"]
        resume.email = request.POST["email"]
        resume.education = request.POST["education"]
        resume.skills = request.POST["skills"]

        resume.save()

        return redirect("view_resume")

    return render(request, "resume.html", {
        "resume": resume
    })
@login_required

@login_required
def dashboard(request):

    resume_count = Resume.objects.filter(user=request.user).count()

    context = {
        "resume_count": resume_count,
    }

    return render(request, "dashboard.html", context)

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

@login_required
def resume_review(request):

    resume = Resume.objects.filter(user=request.user).first()

    suggestions = []

    if len(resume.skills.split(",")) < 5:
        suggestions.append(
            "Add more technical skills to improve your resume."
        )

    if len(resume.education) < 15:
        suggestions.append(
            "Provide more details about your education."
        )

    if len(resume.full_name.split()) < 2:
        suggestions.append(
            "Use your full name instead of only your first name."
        )

    if not suggestions:
        suggestions.append(
            "Great! Your resume looks good."
        )

    return render(
        request,
        "resume_review.html",
        {
            "resume": resume,
            "suggestions": suggestions
        }
    )
@login_required
def interview(request):

    questions = None

    if request.method == "POST":

        role = request.POST["role"]

        questions = generate_interview_questions(role)

    return render(request, "interview.html", {
        "questions": questions
    })
@login_required
def jobs(request):

    jobs = []

    if request.method == "POST":

        skills = request.POST["skills"].lower()

        if "python" in skills:
            jobs.append("Python Developer")

        if "django" in skills:
            jobs.append("Django Developer")

        if "mysql" in skills:
            jobs.append("Backend Developer")

        if "testing" in skills:
            jobs.append("Manual Tester")

        if not jobs:
            jobs.append("No matching jobs found.")

    return render(request, "jobs.html", {
        "jobs": jobs
    })
@login_required
def profile(request):
    return render(request, "profile.html")
@login_required
def delete_resume(request):

    resume = Resume.objects.filter(user=request.user).first()

    if resume:
        resume.delete()

    return redirect("dashboard")


@login_required
def resume_analyzer(request):
    feedback = None

    if request.method == "POST":
        resume = request.POST.get("resume")

        prompt = f"""
        Analyze the following resume.

        Give:
        1. Strengths
        2. Weaknesses
        3. Missing Skills
        4. ATS Score out of 100
        5. Suggestions for Improvement

        Resume:
        {resume}
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        feedback = response.text

    return render(request, "resume_analyzer.html", {
        "feedback": feedback
    })

@login_required
def career_guidance(request):
    advice = None

    if request.method == "POST":
        interests = request.POST.get("interests")

        prompt = f"""
        The student has the following interests:

        {interests}

        Suggest:
        1. Best career paths
        2. Skills to learn
        3. Certifications
        4. Job roles
        5. 6-month roadmap
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        advice = response.text

    return render(request, "career_guidance.html", {
        "advice": advice
    })