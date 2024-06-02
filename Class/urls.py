from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # path('', views.index, name = 'index'),
    path('', views.index, name = 'index'),
    path('student_login', views.student_login, name = 'student_login'),
    path('teacher_login', views.teacher_login, name = 'teacher_login'),
    path('student_dashboard', views.student_dashboard, name = 'student_dashboard'),
    path('teacher_dashboard', views.teacher_dashboard, name = 'teacher_dashboard'),
    path('student_signup', views.student_signup, name = 'student_signup'),
    path('teacher_signup', views.teacher_signup, name = 'teacher_signup'),
    path('logout',views.logout,name='logout'),
    # path('teacher_login', views.teacher_login, name = 'teacher_login'),
    # path('student_detail/<str:courses>/', views.student_detail, name='student_detail'),
    # path('student_detail', views.student_detail, name = 'student_detail'),
    # path('index',views.index,name = 'index'),
    path('about', views.about, name = 'about'),
    path('s_quizzes', views.s_quizzes, name = 's_quizzes'),
    path('s_notes', views.s_notes, name = 's_notes'),
    path('s_notes/<int:subid>', views.s_notess, name = 's_notess'),
    path('s_assignment', views.s_assignment, name = 's_assignment'),
    path('s_assignment/<int:subid>', views.s_assignmentt, name = 's_assignmentt'),
    path('about', views.about, name = 'about'),
    path('t_quizzes/<int:subkey>', views.t_quizzes, name = 't_quizzes'),
    path('t_notes', views.t_notes, name = 't_notes'),
    path('t_notess/<int:subkey>', views.t_notess, name = 't_notess'),
    path('t_assignment/<int:subkey>', views.t_assignment, name = 't_assignment'),
    path('add_note/<int:subkey>', views.add_note, name = 'add_note'),


    # All new path are below
    path('login', views.login_view, name = 'login_view'),
    path('signup', views.signup_view, name = 'signup_view'),
    path('student_details', views.student_details, name = 'student_details'),
    path('hod_login', views.hod_login, name = "hod_login"),
    path('hod_signup', views.hod_signup, name = "hod_signup"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('hod_dashboard', views.hod_dashboard, name='hod_dashboard'),
    path('logout_hod', views.logout_hod, name='Logout_hod'),
    path('admin_edit_teacher', views.admin_edit_teacher, name='admin_edit_teacher'),
    path('admin_edit_courses', views.admin_edit_courses, name='admin_edit_courses'),
    path('admin_edit_subject', views.admin_edit_subject, name='admin_edit_subject'),
    path('add_course', views.add_course, name='add_course'),

    #### password reset urls

    path('forget_password', views.forget_password, name = 'forget_password'),

    path('change_password/<str:token>/', views.change_password, name = 'change_password'),

]