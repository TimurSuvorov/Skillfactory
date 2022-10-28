from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPortal import settings
from NewsPortal.settings import SITE_URL, DEFAULT_FROM_EMAIL
from news.models import Post, Category

from celery import shared_task


# Задание на рассылку подписки
@shared_task
def send_to_subscribers_async(t_pk):
    instance = Post.objects.get(pk=t_pk)
    categories_added = instance.category.all()
    subscribers_data = []
    for category in categories_added:
        subscribers_data += category.subscribers.values_list('username', 'email')
    if subscribers_data:
        for subscr_user, subscr_email in set(subscribers_data):
            if subscr_user != instance.postAuthor.author.username:
                html_content = render_to_string('subscribermessage.html',
                                                {'newpostdata': instance,
                                                 'subscr_user': subscr_user,
                                                 'subscr_email': subscr_email,
                                                 'site_url': SITE_URL
                                                 },
                                                )
                send_mail_function(html_content, subscr_email, subject_email='Update for you')
                print(f'SysInfo: Отправлено письмо по сигналу создания поста: {subscr_user} по адресу {subscr_email}')


# Задание на еженедельную рассылку новостей
@shared_task
def weekly_digest_async():
    week_ago_time = datetime.now( ) - timedelta(weeks=1)
    posts_last_week = Post.objects.filter(cr_time__gte=week_ago_time)
    categories_last_week = set(posts_last_week.values_list('category__catname', flat=True))
    subscribers_last_week = set(Category.objects.filter(catname__in=categories_last_week).values_list('subscribers__pk',
                                                                                                      'subscribers__username',
                                                                                                      'subscribers__email'
                                                                                                      )
                                )
    subscriber_dict = {}  # Составим словари для каждого подписчика со своими новостями
    for subscriber in subscribers_last_week:
        if subscriber[0]:
            subscriber_obj = User.objects.get(pk=subscriber[0])  # Категории, на которые подписан юзер
            # Из ранее отфильтрованных постов фильтруем с нужной категорией
            posts_for_subscriber = list(set(Post.objects.filter(pk__in=posts_last_week,
                                                                category__in=subscriber_obj.category_set.all()
                                                               )
                                            )
                                        )
            subscriber_dict['subcr_username'] = subscriber[1]
            subscriber_dict['subcr_email'] = subscriber[2]
            subscriber_dict['postinstances'] = posts_for_subscriber

            html_content = render_to_string('subscribermessage_weekly.html',
                                            {'subscr_user': subscriber_dict['subcr_username'],
                                             'subscr_email': subscriber_dict['subcr_email'],
                                             'postinstances': subscriber_dict['postinstances'],
                                             'site_url': SITE_URL,
                                             },
                                            )

            send_mail_function(html_content,
                               to_email=subscriber_dict['subcr_email'],
                               body_email='',
                               subject_email='Weekly digest',
                               from_email=DEFAULT_FROM_EMAIL)

            print('SysInfo:Отправлено письмо по с недельным дайджестом:', subscriber_dict['subcr_username'])


# Функция для отправки email с html-шаблоном
def send_mail_function(html_content_email,
                       to_email,
                       body_email='',
                       subject_email='Update message',
                       from_email=settings.DEFAULT_FROM_EMAIL):

    msg = EmailMultiAlternatives(
        subject=subject_email,
        body=body_email,
        from_email=from_email,
        to=[to_email],
    )
    msg.attach_alternative(html_content_email, "text/html")
    msg.send()

