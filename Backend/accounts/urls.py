from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path("dashboard/",views.dashboard, name="dashboard"),
    path("resume/",views.resume_builder, name="resume"),
    path("myresume/",views.view_resume, name="view_resume"),
    path("download/",views.download_resume, name="download_resume"),
    path("review/", views.resume_review, name="resume_review"),
    path("interview/", views.interview, name="interview"),
    path("jobs/", views.jobs, name="jobs"),
    path("profile/", views.profile, name="profile"),
    path("edit_resume/", views.edit_resume, name="edit_resume"),
    path("delete_resume/", views.delete_resume, name="delete_resume"),
    path("resume-analyzer/", views.resume_analyzer, name="resume_analyzer"),
    path("career-guidance/", views.career_guidance, name="career_guidance"),
]