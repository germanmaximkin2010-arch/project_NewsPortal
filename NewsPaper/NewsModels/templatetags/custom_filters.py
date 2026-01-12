from django import template

badwords = ['редиска','картошка']
punctuations = ['.',',']

register = template.Library()


@register.filter()
def censor(post):
    words = post.split()
    for index, word in enumerate(words):
        if word[-1] in punctuations:
            core_word = word[:-1]
        else:
            core_word = word
        if core_word.lower() in badwords:
            if word[-1] in punctuations:
                words[index] = word[0] + '*' * (len(word) - 2) + word[-1]
            else:
                words[index] = word[0] + '*' * (len(word) - 1)
    return ' '.join(words)