from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, CharField, ModelMultipleChoiceField, SelectMultiple
from .models import Post, Author, Category


class PostForm(ModelForm):
    title = CharField(min_length=10, label='Название')
    content = CharField(min_length=10, label='Содержание')
    postAuthor = ModelChoiceField(label='Автор',
                                  empty_label='Выберите автора',
                                  queryset=Author.objects.all(),
                                  )
    category = ModelMultipleChoiceField(label='Категория',
                                        queryset=Category.objects.all(),
                                        widget=SelectMultiple
                                        )

    class Meta:
        model = Post
        fields = ['title', 'content', 'postAuthor', 'category']

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        new_title = cleaned_data.get('title')

        exist_title = Post.objects.filter(title=new_title)
        if exist_title.count() > 0:
            raise ValidationError(
                "Ошибка: Такая статья уже есть"
            )


        return cleaned_data
