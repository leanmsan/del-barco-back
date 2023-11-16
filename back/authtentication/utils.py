import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword

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