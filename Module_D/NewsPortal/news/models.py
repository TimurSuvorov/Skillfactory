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
                                  primary_key=True  # Первичный ключ будет тот же, что и внешний ключ
                                  )

    rating = models.SmallIntegerField(default=0)

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


class Category(models.Model):
    catname = models.CharField(max_length=64,
                               unique=True)
    subscribers =models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f"{self.catname}"

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
                            default='post'
                            )
    cr_time = models.DateTimeField(auto_now_add=True)
    postAuthor = models.ForeignKey(Author, on_delete=models.RESTRICT)
    category = models.ManyToManyField(Category, through='PostCategory')

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
        return reverse('special_post', args=[str(self.id)])


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category.catname}: {self.post.title}"

    def get_absolute_url(self):
        return reverse('special_post', args=[str(self.id)])


class UserCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commUser = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    cr_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

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
