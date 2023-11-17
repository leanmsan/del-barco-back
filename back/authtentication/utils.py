import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings

def generateOtp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    Subject = "Verificación de correo"
    opt_code = generateOtp()
    print(opt_code)
    user = User.objects.get(email=email)
    email_body = f'Hola {user.first_name}! Por favor, verifica tu email con el siguiente codigo: {opt_code}'
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=opt_code)

    email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    email.send(fail_silently=True)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]  
    )
    email.send()