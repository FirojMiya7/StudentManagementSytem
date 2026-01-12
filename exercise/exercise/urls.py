"""
URL configuration for exercise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('recycle/', views.recycle, name='recycle'),
    path('studentRecord/', views.studentRecord, name='studentRecord'),
    path('', views.home, name='home'),
    path('edit/<int:id>/', views.edit_data, name='edit_data'),
    path('delete/<int:id>/', views.delete_data, name='delete_data'),
    path('restore/<int:id>/', views.restore_student, name='restore_student'),
    path('permanent-delete/<int:id>/', views.delete_data_Recycle, name='delete_data_Recycle'),
]
