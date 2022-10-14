from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


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
        # aupostrat = self.post_set.all().aggregate(AuPostRating=Sum('rating')).get('AuPostRating')
        # if aupostrat is None:
        #     aupostrat = 0
        #
        # aucommentrat = self.author.comment_set.all().aggregate(AuCommRating=Sum('rating')).get('AuCommRating')
        # if aucommentrat is None:
        #     aucommentrat = 0
        #
        # aupostcommentrat = 0
        # for xpost in self.post_set.all():
        #     xpostcommrat = xpost.comment_set.all().aggregate(AuPostCommRating=Sum('rating')).get('AuPostCommRating')
        #     if xpostcommrat is None:
        #         xpostcommrat = 0
        #     aupostcommentrat += xpostcommrat
        #
        # self.rating = aupostrat*3 + aucommentrat + aupostcommentrat

        newrating = sum(Post.objects.filter(postAuthor=self).values_list('rating', flat=True)) * 3 + \
                    sum(Comment.objects.filter(commUser__author=self).values_list('rating', flat=True)) + \
                    sum(Comment.objects.filter(post__postAuthor=self).values_list('rating', flat=True))

        self.rating = newrating
        self.save()


class Category(models.Model):
    catname = models.CharField(max_length=64,
                               unique=True)

    def __str__(self):
        return f"{self.catname}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):

    ARTICLE = 'AR'
    NEWS = 'NW'

    TYPES = [
        (ARTICLE, "Пост"),
        (NEWS, "Новость")
    ]

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
        return reverse('special_post' , args=[str(self.id)])


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
