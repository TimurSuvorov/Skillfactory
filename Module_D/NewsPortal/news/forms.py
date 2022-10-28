from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, ModelMultipleChoiceField, SelectMultiple
from .models import Post, Category


class PostForm(ModelForm):
    title = CharField(min_length=3, label='Название')
    content = CharField(min_length=3, label='Содержание')
    category = ModelMultipleChoiceField(label='Категория',
                                        queryset=Category.objects.all(),
                                        widget=SelectMultiple
                                        )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        new_title = cleaned_data.get('title')

        exist_title = Post.objects.filter(title=new_title)
        if exist_title.count() > 0:
            raise ValidationError(
                "Ошибка: Такая статья уже есть"
            )

        return cleaned_data
