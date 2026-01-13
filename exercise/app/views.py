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

