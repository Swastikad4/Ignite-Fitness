from django.urls import path
from authapp import views

urlpatterns = [
    path('',views.Home,name="Home"),
    path('about',views.about,name="About"),
    path('signup',views.signup,name="signup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handleLogout,name="handleLogout"),
    path('contact',views.contact,name="contact"),
    path('join',views.enroll,name="enroll"),
    path('profile',views.profile,name="profile"), 
    path('gallery',views.gallery,name="gallery"),
    path('attendance',views.attendance,name="Attendance"),
    path('Workout',views.Workout,name="Workout"),
    path('question_form', views.ai_explanation, name="ai_explanation")
    
]