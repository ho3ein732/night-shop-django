from django.core.mail import send_mail


def sendMail(mail, token):
    send_mail('NightShop - confirm code', f'Confirm Code : {token}', 'ho3ein.732h@gmail.com', [mail],
              fail_silently=False)
