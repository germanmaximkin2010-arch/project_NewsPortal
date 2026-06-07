import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *

Author1 = Author.objects.get(user_id=2)
Author2 = Author.objects.get(user_id=3)
post_types = ['NW','AR']
Authors = [Author1,Author2]

def gem_post():
    for i in range(3, 50):

        kwargs = {
            'author': random.choice(Authors),
            'type': random.choice(post_types),
            'title': f'заготовка поста{i}',
            'content': f'Содержание поста {i * 3}'
        }
        Post.objects.create(**kwargs)
    print('Всё прошло успешно!')


def send_notification(pk, title, preview, emails):
    html_content = render_to_string(
        'Emails/send_post_created.html',
        {
            'link': f'{settings.SITE_URL}/post/{pk}',
            'title': title,
            'preview': preview,
            'pk': pk
        }
    )
    message = EmailMultiAlternatives(
        subject=title,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails,
    )
    message.attach_alternative(html_content, "text/html")
    message.send()