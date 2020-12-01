import email
from django.core.mail import EmailMessage
import random as r

def otpgen():
    otp=""
    for i in range(4):
        otp+=str(r.randint(1,9))
        print("something>>>>>>>>>")
    return otp


def Email(subject,otp,email_id):
    myemail = EmailMessage(subject,otp, to=[email_id])
    myemail.send()
    return True

