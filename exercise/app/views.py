from email import message
import email
from os import name
from django.shortcuts import render, redirect
from .models import Student
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.


def home(request):
    return render(request, 'home.html')




def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')

        print(name, age, email)

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
    subject = 'Warning: School Fee Not Paid'
    message = f'Hello {student.name},\n\nThis is a warning that your account has been marked for deletion due to non-payment of school fees.\n\nPlease contact the administration to resolve this matter.\n\nThank you!'
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
    subject = 'Account Restored - We Apologize'
    message = f'Hello {student.name},\n\nWe sincerely apologize for the accidental deletion of your account.\n\nYour account has now been restored. If you experience any issues, please contact us.\n\nThank you for your patience!\n\nBest regards,\nAdministration'
    from_email = 'firojali723@gmail.com'            
    recipient_list = [student.email]
            
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return redirect('recycle')


# Permanent/Hard delete function for recycle bin
def delete_data_Recycle(request, id):
    student = Student.objects.get(id=id)
    student.delete()

    subject = 'Account Deleted Due to Non-Payment'
    message = f'Hello {student.name},\n\nYour account has been permanently deleted from our system due to non-payment of school fees.\n\nIf you believe this is an error, please contact the administration immediately.\n\nThank you!'
    from_email = 'firojali723@gmail.com'            
    recipient_list = [student.email]
            
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('recycle')

