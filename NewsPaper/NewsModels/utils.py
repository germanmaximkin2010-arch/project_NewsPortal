import random
from .models import *

Author1 = Author.objects.get(user_id=2)
Author2 = Author.objects.get(user_id=3)
post_types = ['NW','AR']
Authors = [Author1,Author2]

def gem_post():
    for i in range(3, 50):

        kwargs = {
            'author': random.choice(Authors),
            'type': random.choice(post_types),
            'title': f'заготовка поста{i}',
            'content': f'Содержание поста {i * 3}'
        }
        Post.objects.create(**kwargs)
    print('Всё прошло успешно!')