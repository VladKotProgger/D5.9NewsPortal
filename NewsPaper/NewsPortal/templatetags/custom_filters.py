from django import template

register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр только для строк")

    banwords = ['редиска', 'дурак', 'идиот']
    newtext = value.split(' ')
    stext = [i.lower() for i in newtext]

    for banword in banwords:
        for k, word in enumerate(stext):
            if banword in word:
                newtext[k] = word[0] + '*' * (len(word) - 1)

    return ' '.join(newtext)
