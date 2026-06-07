import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Category
from .utils import send_notification


@shared_task
def task_create_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []
    for category in categories:
        sub_users = category.subscribers.all()
        subscribers_emails += [sub.email for sub in sub_users]

    subscribers_emails = list(set(subscribers_emails))

    send_notification(post.pk, post.title, post.preview(), subscribers_emails)


@shared_task
def task_weekly_posts():
    last_week = timezone.now() - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    category = list(set(posts.values_list("category__category", flat=True)))

    subscribers_ids = list(set(Category.objects.filter(category__in=category).values_list("subscribers", flat=True)))

    for subscriber in User.objects.filter(id__in=subscribers_ids):
        subscriber_posts = list(set(posts.filter(category__in=subscriber.categories.all())))

        html_content = render_to_string(
            'Emails/weekly_posts.html',
            {
                'posts': subscriber_posts,
                'username': subscriber.username,
                'link': settings.SITE_URL
            }
        )
        message = EmailMultiAlternatives(
            subject='Новые публикации за последнюю неделю!',
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )
        message.attach_alternative(html_content, "text/html")
        message.send()
    print('Рассылка завершена!')
