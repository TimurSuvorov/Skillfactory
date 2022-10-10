import django_filters
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Category


class NewsFilter(FilterSet):

    title = django_filters.CharFilter(field_name='title',
                                      lookup_expr='icontains',
                                      label='Заголовок'
                                      )

    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        field_name='category__catname',
                                                        label='Категория',
                                                        conjoined=True,
                                                        )

    cr_time = django_filters.DateFilter(field_name='cr_time',
                                        lookup_expr='gt',
                                        label='Время публикации',
                                        widget=DateInput(format='%d/%m/%Y',
                                                         attrs={'type': 'date'},
                                                         ),
                                        )

    # type = django_filters.ChoiceFilter(choices=Post.TYPES,
    #                                    label='Тип',
    #                                    empty_label='Выберите тип'
    #                                    )
