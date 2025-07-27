from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return self.email
    

class Enrollment(models.Model):        
    full_name = models.CharField(max_length=25)
    email = models.EmailField()
    gender = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=12)
    dob = models.DateField(blank=True, null=True)
    membership_plan = models.CharField(max_length=200)
    trainer = models.CharField(max_length=55)
    reference = models.CharField(max_length=55)
    address = models.TextField()
    payment_status = models.CharField(max_length=55, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Trainer(models.Model):
    name = models.CharField(max_length=55)
    gender = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    salary = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class MembershipPlan(models.Model):
    plan = models.CharField(max_length=185)
    price = models.IntegerField()

    def __str__(self):
        return self.plan
    

class Attendance(models.Model):
    select_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    login = models.CharField(max_length=200)
    logout = models.CharField(max_length=200)
    workout = models.CharField(max_length=200)
    trained_by = models.CharField(max_length=200)

    def __str__(self):
        return f"Attendance on {self.select_date}"
    

class Gallery(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='gallery')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Workout(models.Model):
    target_muscle = models.CharField(max_length=25)
    exercise_1 = models.CharField(max_length=25)
    exercise_2 = models.CharField(max_length=25)
    exercise_3 = models.CharField(max_length=25)
    exercise_4 = models.CharField(max_length=25)
    
    def __str__(self):
        return self.target_muscle    


