from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from .password_reset_helper import send_forget_password_mail
from django.db.models import Count
import uuid

My_user = get_user_model()


# Create your views here.
def index(request):
    return render(request, 'index.html')

# Common views

csrf_protect
def signup_view(request):
    if request.method == 'POST':
        # username = request.POST['u_name']
        fName = request.POST['firstName']
        lName = request.POST['lastName']
        e_mail = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirmPassword']
        user_type = request.POST['login_as']

        if password ==confirm:
            if CustomUser.objects.filter(email=e_mail).exists():
                messages.success(request,'User already exists with this email ')
                return redirect('signup_view')
            else:
                if user_type=="student":
                    user = CustomUser.objects.create_user   (username=e_mail, email=e_mail,  password=password, user_type = 3)
                    user.save()
                    stu_user = user.student
                    stu_user.fname = fName
                    stu_user.lname = lName
                    stu_user.save()
                    messages.success(request, "You have Registered Successfully!")
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # return render(request, 'student_dashboard.html')
                    return redirect('student_details')
                else:
                    key=request.POST['idKey']
                    print("Hello I am Here")
                    user = CustomUser.objects.create_user   (username=e_mail, email=e_mail,  password=password, user_type = 2)
                    user.save()
                    teacher_user = user.teacher
                    teacher_user.fname = fName
                    teacher_user.lname = lName
                    teacher_user.id_key = key
                    teacher_user.save()
                    messages.success(request, "You have Registered Successfully!")
                    # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('login_view')
        else:
            messages.info('Enter correct password')
            return redirect('signup_view')
    else:
        return render(request, 'signup.html')
    
csrf_protect
def login_view(request):
    if request.method == 'POST':
        e_mail = request.POST['mail']
        password = request.POST['password']
        user_type = request.POST['login_as']
        user = auth.authenticate(request,email=e_mail, password = password)
        if user != None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            if user_type=="teacher":
                teacher_obj = user.teacher
                context = {'user':user, 'teacher':teacher_obj}
                request.session['context']=context
                return redirect('teacher_dashboard')
            else:
                stu_obj = user.student
                subjects = Subject.objects.filter(sem=stu_obj.sem)
                context = {'user': user, 'student':stu_obj, 'subjects':subjects}
                return render(request,'student_dashboard.html', context)
        else:
            print("error")
            messages.info(request,'Invalid Credentials')
            return redirect('login_view')
    else:
        return render(request, 'login.html')
    

def about(request):
    return render(request, 'about.html')
# def login(request):
#     return render(request,'')

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='/')
def dashboard(request):
    if request.user.user_type=="3" :
        return redirect('student_dashboard')
    elif request.user.user_type=="2":
        teacher_dashboard(request)
    else:
        student_dashboard(request)

def s_notes(request):
    return render(request,'s_notes.html')

def s_notess(request,subid):
    # subject = Subject.objects.filter(id = subid)
    note = Notes.objects.filter(subject_id = subid)
    subject = Subject.objects.get(id = subid)
    return render(request,'s_notes.html',{'notes':note,'subid':subid,'subjects':subject})

def s_assignment(request):
    return render(request,'s_assignment.html')

def s_assignmentt(request, subid):
    assign = Assignment.objects.filter(subject_id = subid)
    return render(request,'s_assignment.html',{'assignments':assign,'subid':subid})

def s_quizzes(request):
    return render(request,'s_quizzes.html')

def t_notes(request,subkey):
    note = Notes.objects.filter(subject_id = subkey)
    return render(request,'t_notes.html')


def t_notess(request,subkey):
    note = Notes.objects.filter(subject_id = subkey)
    return render(request,'t_notes.html')

def t_assignment(request,subkey):
    return render(request,'t_assignment.html')

def t_quizzes(request,subkey):
    return render(request,'t_quizzes.html')

def add_note(request,subkey):
    user_profile = Teacher.objects.get(admin = request.user)
    if request.method =='POST':
        note = request.FILES.get('add_note')
        notes = Notes.objects.create(subject_id = subkey, notes=note)
        notes.save()
        return redirect(request.META.get('HTTP_REFERER'))
    


# Student Views
@login_required
def student_details(request):
    if request.method == 'POST':
        father_name = request.POST['fatherName']
        phone = request.POST['phone']
        dob= request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        course = request.POST['course']
        branch = request.POST['branch']
        sem = request.POST['sem']
        rollNo= request.POST['rollNo']
        course_obj = Courses.objects.get(course_name=course)
        branch_obj = Branch.objects.get(branch_name=branch)

        stu_obj = Student.objects.get(admin = request.user)
        stu_obj.fathername =father_name
        stu_obj.phone_no = phone
        stu_obj.dob = dob
        stu_obj.gender = gender
        stu_obj.address = address
        stu_obj.course = course_obj
        stu_obj.branch = branch_obj
        stu_obj.sem = int(sem)
        stu_obj.rollno = rollNo

        stu_obj.save()
        return redirect('dashboard')

    else:
        return render(request, 'studentdetails.html')

@csrf_protect
def student_signup(request):
    if request.method == 'POST':
        username = request.POST['User_name']
        firstname = request.POST['full_name']
        phone = request.POST['Mobile_no']
        email = request.POST['e_mail']
        password = request.POST['Password']
        password2 = request.POST['confirm']

        if password==password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('student_signup')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email is already used')
                return redirect('student_signup')
            else:
                user = CustomUser.objects.create_user(username=username, first_name=firstname, email=email, password=password, user_type = 3)
                user.save()
                # login(request,user)
                request.session["message"] = str(firstname)
                # request.session["phone"] = int(phone)
                # authenticated_user = auth.authenticate(email=email, password=password)
                # log in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                use = CustomUser.objects.get(email = request.user.email)
                student = Student.objects.get(admin = use)
                student.phone_no = phone
                courses=Courses.objects.all()

                return render(request,'student_detail.html',{'courses':courses})
                # return HttpResponseRedirect(reverse('student_detail', kwargs={'courses':courses}))
        else:
            messages.info(request,'Please enter correct password')
            return redirect('student_signup')
    else:
        return render(request,'student_signup.html')

def student_login(request):
    if request.method == 'POST':
        mail = request.POST['email']
        pas = request.POST['pass']
        user = auth.authenticate(request, email=mail, password = pas)
        if user != None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('student_dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('student_login')
    else:
        return render(request,'student_login.html')
    

# @login_required(login_url='/')
# @csrf_protect
# def student_detail(request):
#     if request.method == 'POST':
#         # fullname = request.POST['full_name']
#         father_name = request.POST['Fathers_name']
#         course_id = request.POST['course']
#         branch = request.POST['branch']
#         year = request.POST['year']
#         semester = request.POST['semester']
#         roll_no = request.POST['roll_no']
#         address = request.POST['address']
#         # user = CustomUser.objects.get(username=request.user.username)
#         # user = stu_detail.objects.get(user=request.user)
#         # user = Studetails.objects.get(user = Student.objects.get(admin = request.user))
#         use = CustomUser.objects.get(email = request.user.email)
#         student = Student.objects.get(admin = use)
#         student.address = address
#         student.fathername = father_name
#         student.branch = branch
#         student.sem = semester
#         student.rollno = roll_no
#         student.year = year
#         # courses=Courses.objects.all()
#         course_obj = Courses.objects.get(id=course_id)
#         # user_stu = Student.object.filter(admin = request.user).first()
#         # user_stu.address = address
#         # user_stu.fathername = father_name
#         # user_stu.branch = branch
#         # user_stu.course = course
#         # user_stu.year = year
#         # user_stu.sem = semester
#         # user_stu.rollno = roll_no  
#         student.save()  
#         return redirect('student_dashboard')
#     else:
#         return render(request, 'student_detail.html')
    
@login_required(login_url='/')
def student_dashboard(request):
    # u = My_user.objects.get(id = request.user.id)
    # name = Student.get(admin = request.user)
    # context = {'name':My_user.student_set.get(id = request.user.id).username}
    use = CustomUser.objects.get(email = request.user.email)
    student = Student.objects.get(admin = use)
    subject = Subject.objects.all()
    nm = request.user.first_name
    context = {'name':nm,'branch':student.branch,'course':student.course_id.course_name,'roll':student.rollno,'profile':student.profile_pic,'subjects':subject}
    return render(request,'student_dashboard.html',context)

    


#Teacher Views
def teacher_login(request):
    if request.method == 'POST':
        # username = request.POST['u_name']
        e_mail = request.POST['mail']
        password = request.POST['password']
        user = auth.authenticate(request,email=e_mail, password = password)
        if user != None:
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('teacher_dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('teacher_login')
    else:
        return render(request,'teacher_login.html')
    

def teacher_signup(request):
    if request.method == 'POST':
        username = request.POST['User_name']
        firstname = request.POST['full_name']
        phone_no = request.POST['Mobile_no']
        email = request.POST['e_mail']
        password = request.POST['Password']
        password2 = request.POST['confirm']
        if password==password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('teacher_signup')
            elif CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email is already used')
                return redirect('teacher_signup')
            else:
                user = CustomUser.objects.create_user(username=username, first_name=firstname, email=email, password=password, user_type = 2)
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                use = CustomUser.objects.get(email = request.user.email)
                teacher = Teacher.objects.get(admin = use)
                Teacher.phone = phone_no
                return redirect('teacher_dashboard')
        else:
            messages.info(request,'Please enter correct password')
            return redirect('teacher_signup')
    else:
        return render(request,'teacher_signup.html')
    

@login_required(login_url='/')
def teacher_dashboard(request):
    use = CustomUser.objects.get(email = request.user.email)
    teacher = Teacher.objects.get(admin = use)
    nm = request.user.first_name
    subject = Subject.objects.filter(teacher_id = request.user.id)
    # subject = Subject.objects.all()
    context = {'name':nm,'subjects':subject}
    return render(request,'teacher_dashboard.html',context)



#HOD views

csrf_protect
def hod_signup(request):
    if request.method == 'POST':
        # username = request.POST['User_name']
        # firstname = request.POST['full_name']
        # phone_no = request.POST['Mobile_no']
        email = request.POST['mail']
        password = request.POST['Password']
        password2 = request.POST['confirm']
        if password==password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'Email is already used')
                return redirect('hod_signup')
            else:
                user = CustomUser.objects.create_user(email=email, password=password, username=email, user_type = 1)
                user.save()
                hod_obj = user.hod
                hod_obj.uniqueID = uuid.uuid4()
                hod_obj.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Your HOD id is: '+str(hod_obj.uniqueID)+'\nSave this id for future use.')
                return redirect('hod_dashboard')
        else:
            messages.info(request,'Please enter correct password')
            return redirect('hod_signup')
    else:
        return render(request,'admin_signup.html')
    

@csrf_protect
def hod_login(request):
    if request.method == 'POST':
        # username = request.POST['u_name']
        e_mail = request.POST['mail']
        password = request.POST['password']
        user = auth.authenticate(request,email=e_mail, password = password)
        print(user.user_type)
        if user != None and user.user_type=="1":
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('hod_dashboard')
        else:
            print(type(user.user_type))
            messages.info(request,'Invalid Credentials')
            return redirect('hod_login')
    else:
        return render(request,'adminlogin.html')
        

def logout_hod(request):
    auth.logout(request)
    return redirect('/hod_login')

def add_course(request):
    pass

@login_required(login_url='/hod')
def hod_dashboard(request):
    # use = CustomUser.objects.get(email = request.user.email)
    # teacher = Teacher.objects.get(admin = use)
    # nm = request.user.first_name
    # subject = Subject.objects.filter(teacher_id = request.user.id)
    # # subject = Subject.objects.all()
    # context = {'name':nm,'subjects':subject}
    return render(request,'adminhome.html')

def admin_edit_teacher(request):
    if request.method == 'POST':
        teacher = request.POST['tName']
        keyId = request.POST['keyId']
        subjects = request.POST['subjects']
        messages.success(request, 'Teacher added successfully')
    else:
        subjects = Subject.objects.filter(hod=request.user.hod)
        teachers = Teacher.objects.filter(hod=request.user.hod)
        context={'subjects':subjects, 'teachers':teachers, 'Subject':Subject}
        return render(request, 'admineditteacher.html',context)

def admin_edit_courses(request):
    if request.method =='POST':
        course = request.POST['courseName']
        branch = request.POST['branchName']
        semCount = request.POST['semCount']
        course_obj = Courses(course_name = course, total_sem = semCount)
        course_obj.save()
        branch_obj = Branch(branch_name=branch, course=course_obj, hod=request.user.hod)
        branch_obj.save()
        messages.success(request, 'Course added Successfully')
        return redirect('admin_edit_courses')
    else:
        courses = Courses.objects.annotate(branch_count=Count('branch'))
        context={'courses':courses}
        return render(request, 'admineditcourses.html', context)

def admin_edit_subject(request):
    return render(request, 'admineditsubject.html')

### Forget Password Views

def change_password(request, token):
    context={}
    try:
        user_obj = CustomUser.objects.get(forget_password_token = token)
        print(user_obj)
        if request.method=='POST':
            new_pass = request.POST['password']
            confirm_pass = request.POST['confirm']
            # user_id= request.POST['user_id']
            if new_pass != confirm_pass:
                messages.success('Password does not matches')
                return redirect(f'change_password/{token}/')

        # context = {'user_id': }
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect(request, 'login')

    except Exception as e:
        print(e)
    return render(request, 'changepassword.html', context)

def forget_password(request):
    try:
        if(request.method=='POST'):
            email = request.POST['email']
            if not CustomUser.objects.filter(email = email).first():
                messages.success(request, 'User does not exists with this email')
                return redirect(request,'forget_password')
            user_obj = CustomUser.objects.get(email = email)
            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj, token)
            messages.success(request, 'An email is sent')
            return redirect(request,'forget_password')
    except Exception as e:
        print(e)
    return render(request, 'forgetpassword.html')


