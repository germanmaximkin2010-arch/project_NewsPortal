from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from pyexpat.errors import messages

from .models import Category
from .views import Post

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

@receiver(m2m_changed, sender=Post.category.through)
def send_create_post(sender, instance, action, **kwargs):
    if action != 'post_add':
        return

    categories = instance.category.all()
    subscribers_emails = []
    for category in categories:
        sub_users = category.subscribers.all()
        subscribers_emails += [sub.email for sub in sub_users]

    subscribers_emails = list(set(subscribers_emails))

    send_notification(instance.pk, instance.title, instance.preview(), subscribers_emails)