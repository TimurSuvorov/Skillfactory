from pprint import pprint

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPortal import settings
from NewsPortal.settings import SITE_URL
from .models import PostCategory, Category, Post
from django.contrib.auth.middleware import AuthenticationMiddleware

@receiver(m2m_changed, sender=PostCategory)
def send_to_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories_added = kwargs['pk_set']
        subscribers_data = []
        for category in categories_added:
            subscribers_data += Category.objects.get(pk=category).subscribers.values_list('username', 'email')
        if subscribers_data:
            for subscr_user, subscr_email in set(subscribers_data):
                html_content = render_to_string('subscribermessage.html',
                                                {'newpostdata': instance,
                                                 'subscr_user': subscr_user,
                                                 'subscr_email': subscr_email,
                                                 'site_url': SITE_URL
                                                 },
                                                )
                send_mail_function(html_content, subscr_email)
                print('SysInfo:Отправлено письмо по сигналу создания поста:', subscr_user)

@receiver(post_save, sender=User)
def new_user_signal(sender, instance, **kwargs):

    send_mail(
        subject=f'Привет {instance.username}!',
        message=f'Привет {instance.username}! Добро пожаловать на наш новостной сайт!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email]
    )

    print(f'SysInfo: Отправлено письмо новому пользователю {instance.username}')


@receiver(post_delete, sender=Post)
def post_delete_signal(sender, instance, **kwargs):

    print('Post delete signal')


# Функция для отправки email
def send_mail_function(html_content_email, to_email, body_email='',
                       subject_email='Update for you', from_email=settings.DEFAULT_FROM_EMAIL):
    msg = EmailMultiAlternatives(
        subject=subject_email,
        body=body_email,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content_email, "text/html")
    msg.send()
