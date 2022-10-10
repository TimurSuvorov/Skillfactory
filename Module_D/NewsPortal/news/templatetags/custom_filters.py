from django import template

from ..extension import BADWORDS

register = template.Library()

@register.filter()
def censor(value:str, symbol='*')->str:
    badwords_in_text = set(value.split( )) & set(BADWORDS)  #  Список нецензурных слов в тексте путем пересечения множеств
    if badwords_in_text:
        for badword in badwords_in_text:
            censored = badword[0] + (len(badword) - 1) * symbol
            value = value.replace(badword, censored)
    return value

@register.filter()
def post_type(type_value):
    types = {'AR': "Пост", 'NW': "Новость"}
    return types[type_value]