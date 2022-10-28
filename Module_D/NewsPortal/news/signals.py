from pprint import pprint

from allauth.account.models import EmailAddress
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver

from NewsPortal import settings
from .models import PostCategory, Post
from .tasks import send_to_subscribers_async


# Сигнал добавления поста
@receiver(m2m_changed, sender=PostCategory)
def send_to_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_to_subscribers_async.apply_async([instance.pk], expires=120)


# Сигнал нового пользователя(прохождение верификации)
@receiver(post_save, sender=EmailAddress)
def new_user_signal(sender, instance, **kwargs):
    if instance.verified:  # Когда проведена верификация по email
        send_mail(
            subject=f'Привет {instance.user}!',
            message=f'Привет {instance.user}! Добро пожаловать на наш новостной сайт!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email]
        )

        print(f'SysInfo: Отправлено письмо новому пользователю {instance.user}')


# Функция для отправки email
def send_mail_function(html_content_email, to_email, body_email='',
                       subject_email='Update for you', from_email=settings.DEFAULT_FROM_EMAIL):
    msg = EmailMultiAlternatives(
        subject=subject_email,
        body='',
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content_email, "text/html")
    msg.send()
