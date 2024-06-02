# Generated by Django 5.0.4 on 2024-06-01 12:33

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HOD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uniqueID', models.UUIDField(default=uuid.uuid4)),
                ('profile_pic', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=30)),
                ('sem', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Class.courses')),
                ('hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.hod')),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notes', models.FileField(upload_to='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_name', models.CharField(max_length=50, null=True)),
                ('questions', models.TextField()),
                ('answers', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(default='Teacher', max_length=30)),
                ('lname', models.CharField(default='', max_length=30)),
                ('id_key', models.CharField(max_length=15, null=True)),
                ('profile_pic', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('phone', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.hod')),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.teacher'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.CharField(blank=True, choices=[(1, 'HOD'), (2, 'Teacher'), (3, 'Student')], default=3, max_length=10)),
                ('forget_password_token', models.CharField(max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='admin',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(default='Student', max_length=30)),
                ('lname', models.CharField(default='', max_length=30)),
                ('profile_pic', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('address', models.CharField(default='address', max_length=50)),
                ('fathername', models.CharField(default='fname', max_length=30)),
                ('dob', models.DateField(null=True)),
                ('phone_no', models.IntegerField(default=0)),
                ('branch', models.CharField(default='branch', max_length=30)),
                ('year', models.IntegerField(default=1)),
                ('rollno', models.IntegerField(default=1)),
                ('sem', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Class.courses')),
                ('hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Class.hod')),
                ('admin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hod',
            name='admin',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
