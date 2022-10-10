from django import template

register = template.Library()

@register.simple_tag(takes_context=True)  # Регистрируем тег и говорим, что для работы тега требуется передать контекст
def urlreplacer(context, **kwargs):
    req_param = context['request'].GET.copy()  # request.GET содержит QueryDict
    for k, v in kwargs.items():  # Добавляем в "старый" QueryDict новые значения при переходе
        req_param[k] = v
    return req_param.urlencode()
