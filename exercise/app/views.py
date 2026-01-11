from django.shortcuts import render, redirect
from .models import Student

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
        return redirect('studentRecord')
    return render(request, 'register.html')


def recycle(request):
    return render(request, 'recycle.html')



def studentRecord(request):
    students = Student.objects.filter(is_deleted=False).order_by('name')
    return render(request, 'studentRecord.html', {'students': students})


def delete_data(request, id):
    student = Student.objects.get(id=id)
    student.is_deleted = True
    student.save()
    return redirect('studentRecord')

def recycle(request):
    deleted_students = Student.objects.filter(is_deleted=True).order_by('name')
    return render(request, 'recycle.html', {'deleted_students': deleted_students})

def restore_student(request, id):
    student = Student.objects.get(id=id)
    student.is_deleted = False
    student.save()
    return redirect('recycle')


# Permanent/Hard delete function for recycle bin
def delete_data_Recycle(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect('recycle')
    student.delete()
    return redirect('recycle')