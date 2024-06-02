from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Courses,Student,Teacher,Subject,Notes,Assignment



# class UserModel(UserAdmin):
#     pass


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Courses)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Notes)
admin.site.register(Assignment)
# admin.site.register(CustomUser, UserModel)
# admin.site.register(CustomUser, UserModel)