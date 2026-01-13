from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Student

# Create your views here.


def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not email or not password or not confirm_password:
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'signup.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        login(request, user)
        messages.success(request, 'Account created and logged in successfully.')
        return redirect('studentRecord')

    return render(request, 'signup.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')

        print(name, age, email)

        # Block registration for this specific name.
        if name and name.strip().lower() == "trishan shrestha":
            return HttpResponse("This name is not allowed to register.", status=400)

        Student.objects.create(
                name=name,
                age=age,
                email=email            
            )

        # Send email notification
        subject = 'Registration Successful'
        message = f'Hello {name},\n\nYou have been successfully registered in our system.\n\nThank you!'
        from_email = 'firojali723@gmail.com'            
        recipient_list = [email]
            
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
        return redirect('studentRecord')
    
    return render(request, 'register.html')


def studentRecord(request):
    students = Student.objects.filter(is_deleted=False).order_by('name')
    return render(request, 'studentRecord.html', {'students': students})


def edit_data(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.age = request.POST.get('age')
        student.email = request.POST.get('email')
        student.save()
        return redirect('studentRecord')
    return render(request, 'edit.html', {'student': student})


def delete_data(request, id):
    student = Student.objects.get(id=id)
    student.is_deleted = True
    student.save()
    
   

    subject = 'Account Marked for Deletion'
    message = f'Hello {student.name},\n\nYour account has been marked for deletion.\n\nDon\'t worry! You can restore your account anytime from the recycle bin.\n\nThank you!'
    from_email = 'firojali723@gmail.com'            
    recipient_list = [student.email]
            
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('studentRecord')


def recycle(request):
    deleted_students = Student.objects.filter(is_deleted=True).order_by('name')
    return render(request, 'recycle.html', {'deleted_students': deleted_students})

def restore_student(request, id):
    student = Student.objects.get(id=id)
    student.is_deleted = False
    student.save()
    subject = 'Account Restored'
    message = f'Hello {student.name},\n\nYour account has been successfully restored.\n\nThank you!'
    from_email = 'firojali723@gmail.com'            
    recipient_list = [student.email]
            
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('recycle')


# Permanent/Hard delete function for recycle bin
def delete_data_Recycle(request, id):
    student = Student.objects.get(id=id)
    student.delete()

    subject = 'Account Deleted'
    message = f'Hello {student.name},\n\nYour account has been permanently deleted from our system.\n\nThank you!'
    from_email = 'firojali723@gmail.com'            
    recipient_list = [student.email]
            
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('recycle')

