import re

from django import template

from ..extension import BADWORDS

register = template.Library()

@register.filter()
def censor(value: str, symbol='*'):
    badwords_in_text = set(value.lower().split()) & set(BADWORDS)  # Проверка, есть ли плохие слова в тексте
    if badwords_in_text:
        for badword in badwords_in_text:
            badword_pattern_up = r"\b" + re.escape(badword.capitalize()) + r"\b"  # Для слов с заглавной буквы
            badword_pattern_low = r"\b" + re.escape(badword) + r"\b"  # Для слов с строчной буквы
            value = re.sub(badword_pattern_up, badword.capitalize()[0] + (len(badword) - 2) * symbol + badword[-1], value)
            value = re.sub(badword_pattern_low, badword[0] + (len(badword) - 2) * symbol + badword[-1], value)
    return value

@register.filter()
def typetorus(type_value):
    types = {'AR': "Пост", 'NW': "Новость"}
    return types[type_value]

@register.filter()
def typetoeng(type_value):
    types = {'AR': "article", 'NW': "news"}
    return types[type_value]
