

from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_mail(email, token):
    
    subject = "Reset Your Password"
    message = f'Hello,\nSomeone has requested to reset the password for your Class Tutorial account. If this is you then click the below link to reset password:\n http://127.0.0.1:8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

