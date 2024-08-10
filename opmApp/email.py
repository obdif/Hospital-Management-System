from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email.',
    'olamidedevops@gmail.com',
    ['adeblessinme4u@gmail.com'],
    fail_silently=False,
)

print (send_mail)