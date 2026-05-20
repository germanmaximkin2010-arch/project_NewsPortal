import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from NewsModels.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
