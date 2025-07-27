import os

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from authapp.models import Contact, MembershipPlan, Trainer, Enrollment, Gallery, Attendance
import google.generativeai as genai


# Securely set OpenAI API key from environment variable


# Home Page
def Home(request):
    return render(request, "index.html")

# About Page
def about(request):
    return render(request, "about.html")

# User Signup
def signup(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if len(username) != 10:
            messages.info(request, "Phone Number Must be 10 Digits")
            return redirect('/signup')

        if pass1 != pass2:
            messages.info(request, "Passwords do not match")
            return redirect('/signup')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Phone Number is Taken")
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is Taken")
            return redirect('/signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "User is created. Please log in.")
        return redirect('/login')

    return render(request, "signup.html")

# Handle User Login
def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('usernumber')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
    return render(request, "handlelogin.html")






def Workout(request):
    if request.method == "POST":
        Target_muscle = request.POST.get('Workout')
        Exercise_1 = request.POST.get('1')
        Exercise_2 = request.POST.get('2')
        Exercise_3 = request.POST.get('3')
        Exercise_4 = request.POST.get('4')
        myquery = Workout(
            Target_muscle=Target_muscle,
            Exercise_1=Exercise_1,
            Exercise_2=Exercise_2,
            Exercise_3=Exercise_3,
            Exercise_4=Exercise_4
        )
        myquery.save()
        messages.info(request, "Workout split is saved for future reference.")
    return render(request, "Workout.html")

# Handle User Logout
def handleLogout(request):
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')

# Contact Form
def contact(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('num')
        desc = request.POST.get('desc')
        myquery = Contact(name=name, email=email, phonenumber=number, description=desc)
        myquery.save()
        messages.info(request, "Thanks for contacting us. We will get back to you soon.")
    return render(request, "Contact.html")

# User Enrollment
def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')

    Membership = MembershipPlan.objects.all()
    SelectTrainer = Trainer.objects.all()
    context = {"Membership": Membership, "SelectTrainer": SelectTrainer}

    if request.method == "POST":
        FullName = request.POST.get('FullName')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        PhoneNumber = request.POST.get('PhoneNumber')
        DOB = request.POST.get('DOB')
        member = request.POST.get('member')
        trainer = request.POST.get('trainer')
        reference = request.POST.get('reference')
        address = request.POST.get('address')
        query = Enrollment(
            FullName=FullName, Email=email, Gender=gender, PhoneNumber=PhoneNumber,
            DOB=DOB, SelectMembershipplan=member, SelectTrainer=trainer,
            Reference=reference, Address=address
        )
        query.save()
        messages.success(request, "Thanks for enrolling.")
        return redirect('/join')

    return render(request, "enroll.html", context)

# User Profile
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')
    
    user_phone = request.user.username
    posts = Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance = Attendance.objects.filter(phonenumber=user_phone)
    context = {"posts": posts, "attendance": attendance}
    return render(request, "profile.html", context)

# Gallery
def gallery(request):
    posts = Gallery.objects.all()
    context = {"posts": posts}
    return render(request, "gallery.html", context)

# Attendance
def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in and try again.")
        return redirect('/login')

    SelectTrainer = Trainer.objects.all()
    context = {"SelectTrainer": SelectTrainer}

    if request.method == "POST":
        phonenumber = request.POST.get('PhoneNumber')
        Login = request.POST.get('logintime')
        Logout = request.POST.get('loginout')
        SelectWorkout = request.POST.get('workout')
        TrainedBy = request.POST.get('trainer')
        query = Attendance(
            phonenumber=phonenumber, Login=Login, Logout=Logout, 
            SelectWorkout=SelectWorkout, TrainedBy=TrainedBy
        )
        query.save()
        messages.warning(request, "Attendance applied successfully.")
        return redirect('/attendance')

    return render(request, "attendance.html", context)

from django.shortcuts import render
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyAD6HsTW6uUEcT5OE7hNv0XZL8aT7U-Gyw")

def ai_explanation(request):
    """
    Handles user input and fetches AI explanation from the Gemini API.
    """
    if request.method == "POST":
        user_input = request.POST.get("question")
        if not user_input:
            return render(request, "error.html", {"error_message": "No input provided."})

        try:
            # Initialize the Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")
            # Generate content based on user input
            response = model.generate_content(user_input)
            answer = response.text

            # Pass the response to the HTML template
            return render(request, "answer.html", {"question": user_input, "answer": answer})
        except Exception as e:
            return render(request, "error.html", {"error_message": str(e)})

    # If GET request, render the input form
    return render(request, "question_form.html")




