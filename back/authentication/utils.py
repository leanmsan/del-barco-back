import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings
from django.template.loader import render_to_string
import secrets
import string

def generateAlphanumericOtp():
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphanumeric_chars) for _ in range(8))

def send_code_to_user(email):
    subject = "Verificación de correo"
    opt_code = generateAlphanumericOtp()
    #print(opt_code)
    user = User.objects.get(email=email)

    # Renderizar el cuerpo del correo electrónico como HTML
    email_body_html = render_to_string('email_confirmation.html', {'user': user, 'verification_code': opt_code})

    OneTimePassword.objects.create(user=user, code=opt_code)

    email = EmailMessage(
        subject=subject,
        body=email_body_html,  # Utilizar el cuerpo HTML
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email.content_subtype = "html"  # Indicar que el contenido es HTML
    email.send(fail_silently=True)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]  
    )
    email.send()