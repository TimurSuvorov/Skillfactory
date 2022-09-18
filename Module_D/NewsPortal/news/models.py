from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rate = models.IntegerField(default=0)
    username = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    primary_key=True  # Первичный ключ будет тот же, что и внешний ключ
                                    )

# newrate calculating
# for author_ in Author.objects.all().values_list('username_id', flat=True):
#     newrate = sum(Post.objects.filter(author_id = author_).values_list('rate', flat=True))*3 + \
#               sum(Comment.objects.filter(author_id = author_).values_list('rate', flat=True)) + \
#               sum(Comment.objects.filter(post_id__author_id = author_).values_list('rate', flat=True))
#     au = Author.objects.get(username_id=author_)
#     au.update_rating(newrate)
#     au.save()


    def update_rating(self, newrate):
        self.rate = newrate

class Category(models.Model):
    catname = models.CharField(max_length=255,
                               unique=True
                               )


class Post(models.Model):

    TYPES = [
        ('post', "Пост"),
        ('news', "Новость")
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.IntegerField(default=0)
    type = models.CharField(max_length=10,
                            choices=TYPES,
                            blank=True,
                            null=True
                            )
    cr_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post')
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.content[:124] + "..."

    def like(self):
        self.rate += 1

    def dislike(self):
        self.rate -= 1



class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    cr_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate += 1

    def dislike(self):
        self.rate -= 1

