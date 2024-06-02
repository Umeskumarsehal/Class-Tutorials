from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _  
from django.utils.crypto import get_random_string
from datetime import datetime, timezone
import uuid


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_type_data=((1,"HOD"),(2,"Teacher"),(3,"Student"))
    USERNAME_FIELD = 'email'
    user_type=models.CharField(default=3,choices=user_type_data,max_length=10,blank=True,)

    forget_password_token = models.CharField(max_length= 100, null=True)
    REQUIRED_FIELDS = [email]

    def __str__(self):
        return self.email


#HOD
class HOD(models.Model):
    id=models.AutoField(primary_key=True)
    uniqueID = models.UUIDField(max_length=255, default = uuid.uuid4)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png')
    admin=models.OneToOneField(CustomUser,null = True, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    

    def __str__(self):
        return self.admin.email


#Teacher
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50, default="Teacher")
    lname = models.CharField(max_length=50, default="")
    id_key = models.CharField(max_length=100, null=True)
    admin=models.OneToOneField(CustomUser,null = True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png')
    phone = models.IntegerField(default = 1)
    hod = models.ForeignKey(HOD,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.first_name


#Courses
class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    total_sem = models.IntegerField(default=6)
    # updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def __str__(self):
        return self.course_name
    
#Branch
class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100, null=True)
    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING,null = True)
    hod=models.OneToOneField(HOD, on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
        return self.branch_name


#Student
class Student(models.Model):
    id=models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30, default="Student")
    lname = models.CharField(max_length=30, default="")
    
    admin=models.OneToOneField(CustomUser,null = True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.png')
    address = models.CharField(max_length=50,default="address")
    fathername = models.CharField(max_length=30,default="fname")
    dob = models.DateField(null=True)
    phone_no = models.IntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, null=True)
    year = models.IntegerField(default=1)
    rollno = models.IntegerField(default=1)
    sem = models.IntegerField(default = 1)
    gender = models.CharField(max_length=10, default="Male")
    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING,null = True)
    hod = models.ForeignKey(HOD,null=True, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.fname


#Subject
class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=30)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    sem = models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    hod = models.ForeignKey(HOD,null=True, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    objects = models.Manager()
    def __str__(self):
        return self.subject_name


class Notes(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null = True)
    notes = models.FileField(upload_to='Notes')
    created_at=models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    id=models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=50, null=True)
    subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE,null = True)
    questions = models.TextField()
    answers = models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    Quiz_name = models.CharField(max_length=50, default="Quiz")
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null = True)







    

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            HOD.objects.create(admin=instance)
        if instance.user_type==2:
            Teacher.objects.create(admin=instance)
        if instance.user_type==3:
            Student.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.hod.save()
    if instance.user_type==2:
        instance.teacher.save()
    if instance.user_type==3:
        instance.student.save()