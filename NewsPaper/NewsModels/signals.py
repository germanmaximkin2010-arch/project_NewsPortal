from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import task_create_post


@receiver(m2m_changed, sender=PostCategory)
def send_create_post(sender, instance, action, **kwargs):
    if action != 'post_add':
        return

    task_create_post.delay(instance.pk)
