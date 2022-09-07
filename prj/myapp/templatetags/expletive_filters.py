from django import template

register = template.Library()


@register.filter(
    name='censor'
)
def censor(value):
    with open(r'C:\Users\som\Documents\курс\модуль D2\2.7\TaskModuleD2\prj\myapp\templatetags\badwords.txt', 'r') as file:
        for word in file:
            word = word.rstrip().lower()
            if word in value.lower():
                length = len(word)
                value = value.replace(word, '*' * length)
        return value
