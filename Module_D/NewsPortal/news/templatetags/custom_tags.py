from django import template
from news.models import Post, Author

register = template.Library()

@register.simple_tag(takes_context=True)  # Регистрируем тег и говорим, что для работы тега требуется передать контекст
def urlreplacer(context, **kwargs):
    req_param = context['request'].GET.copy()  # request.GET содержит QueryDict
    for k, v in kwargs.items():  # Добавляем в "старый" QueryDict новые значения при переходе
        req_param[k] = v
    return req_param.urlencode()

@register.simple_tag()
def call_like(pk):
    post = Post.objects.get(pk=pk)
    post.like()
    return f''

@register.simple_tag()
def call_dislike(pk):
    post = Post.objects.get(pk=pk)
    return post.like()

@register.inclusion_tag('news/tags_welcome_user.html', takes_context=True, name='welcome-user')
def welcome_user(context):
    request = context['request']
    isauthor = all([Author.objects.filter(author__username=request.user).exists(),
                    request.user.groups.filter(name='authors').exists()]
                   )
    return {'request': request, 'isauthor': isauthor}