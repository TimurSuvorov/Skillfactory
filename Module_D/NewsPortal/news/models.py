from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating = models.SmallIntegerField(default=0)
    username = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    primary_key=True  # Первичный ключ будет тот же, что и внешний ключ
                                    )

# newrating calculating
# for author_ in Author.objects.all().values_list('username_id', flat=True):
#     newrating = sum(Post.objects.filter(author_id = author_).values_list('rating', flat=True))*3 + \
#               sum(Comment.objects.filter(author_id = author_).values_list('rating', flat=True)) + \
#               sum(Comment.objects.filter(post_id__author_id = author_).values_list('rating', flat=True))
#     au = Author.objects.get(username_id=author_)
#     au.update_rating(newrating)
#     au.save()


    def update_rating(self, newrating):
        self.rating = newrating

class Category(models.Model):
    catname = models.CharField(max_length=64,
                               unique=True
                               )


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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.content[:124] + "..."

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1



class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    cr_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

