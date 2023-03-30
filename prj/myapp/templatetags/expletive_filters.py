import os
from django import template

register = template.Library()


@register.filter(
    name='censor'
)
def censor(value):
    with open(os.path.join(os.path.dirname(__file__), '.', 'badwords.txt'), 'r') as file:
        for word in file:
            word = word.rstrip().lower()
            if word in value.lower():
                length = len(word)
                value = value.replace(word, '*' * length)
        return value
