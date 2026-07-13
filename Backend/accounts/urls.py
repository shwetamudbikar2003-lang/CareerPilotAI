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
]