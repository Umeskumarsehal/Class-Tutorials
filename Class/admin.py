from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *



# class UserModel(UserAdmin):
#     pass


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(HOD)
admin.site.register(Courses)
admin.site.register(Branch)
admin.site.register(Subject)
admin.site.register(Notes)
admin.site.register(Assignment)