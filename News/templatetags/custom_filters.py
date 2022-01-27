from django import template
import re
import random


register = template.Library()

STOP_LIST = [
    'жопа',
    'хуй',
    'пиздец',
]

SYMBOLS = ['*', '!', '#']


@register.filter(name='censor')
def censor(text: str):
    words = text.split(' ')
    new_words = []

    for i, word in enumerate(words):
        match = re.match(f"^{'|'.join(STOP_LIST)}", word)

        if match is not None:
            new_words.append(''.join([random.choice(SYMBOLS)] * len(word)))
        else:
            new_words.append(word)

    return ' '.join(new_words)