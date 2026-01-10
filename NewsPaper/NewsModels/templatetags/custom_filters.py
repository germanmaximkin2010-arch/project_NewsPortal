from string import punctuation

from django import template

badwords = ['редиска','политику','картошка']
punctuations = ['.',',']

register = template.Library()


@register.filter()
def censor(post):
    words = post.split()
    for index, word in enumerate(words):
        if word.lower() in badwords:
            if word[-1] in punctuations:
                words[index] = word[0] + '*' * len(word - 2)
            else:
                words[index] = word[0] + '*' * len(word - 1)
    return words