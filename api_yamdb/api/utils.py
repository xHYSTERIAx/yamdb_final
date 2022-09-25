import random
import string

from django.core.mail import send_mail


def gen_confirmation_code():
    letters = string.ascii_lowercase
    key: int = 10
    return ''.join(random.choice(letters) for i in range(key))


def send_confirmation_code(email, confirmation_code):
    send_mail(
        subject='Подтверждение регистрации на Yamdb',
        message='Спасибо за регистрацию!'
                f'Ваш код подтверждения: {confirmation_code}',
        from_email='register@yambd.com',
        recipient_list=[email],
        fail_silently=False,
    )
