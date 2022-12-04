from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

ARTICLE = 'AR'
NEWS = 'NW'

TYPES = [
    (ARTICLE, "Пост"),
    (NEWS, "Новость")
]


class Author(models.Model):
    author = models.OneToOneField(User,
                                  on_delete=models.CASCADE,
                                  primary_key=True,  # Первичный ключ будет тот же, что и внешний ключ
                                  verbose_name='Автор'
                                  )

    rating = models.SmallIntegerField(default=0,
                                      verbose_name='Рейтинг'
                                      )

    def __str__(self):
        return f"{self.author}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def update_rating(self):
        newrating = sum(Post.objects.filter(postAuthor=self).values_list('rating', flat=True)) * 3 + \
                    sum(Comment.objects.filter(commUser__author=self).values_list('rating', flat=True)) + \
                    sum(Comment.objects.filter(post__postAuthor=self).values_list('rating', flat=True))

        self.rating = newrating
        self.save()

    @property
    def postnumber(self):
        num = len(self.post_set.all())
        return num


class Category(models.Model):
    catname = models.CharField(max_length=64,
                               unique=True,
                               verbose_name='Категория')
    subscribers = models.ManyToManyField(User,
                                         through='UserCategory',
                                         verbose_name='Подписчики')

    def __str__(self):
        return f"{self.catname}"

    def get_absolute_url(self):
        return reverse('category_list', args=[str(self.pk)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):

    title = models.CharField(max_length=254)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    type = models.CharField(max_length=10,
                            choices=TYPES,
                            blank=True,
                            null=True,
                            default='post',
                            verbose_name='Тип'
                            )
    cr_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    postAuthor = models.ForeignKey(Author, on_delete=models.RESTRICT, verbose_name='Автор')
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def preview(self):
        return self.content[:123] + "..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('special_post', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save()
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Пост-Категория"
        verbose_name_plural = "Пост-Категория"

    def __str__(self):
        return f"{self.category.catname}: {self.post.title}"

    def get_absolute_url(self):
        return reverse('special_post', args=[str(self.id)])


class UserCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    commUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    content = models.TextField(blank=False, verbose_name='Содержание')
    cr_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return f"{self.content}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class UserInfo(models.Model):
    country = models.CharField(max_length=124,
                               default='na',
                               verbose_name='Страна'
                               )
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь'
                                )
