# -*- coding: utf-8 -*-

from random import choice

images_people = [
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia2.jpg', 'Caption 1'),
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia3.jpg', 'Caption 2'),
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia4.jpg', 'Caption 3'),
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia-children.jpg', 'Caption 4'),
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/ElZocalo.jpg', 'Caption 5'),
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/israel.jpg', 'Caption 6',)
]

def images(request):
    # return {'frase': 'Niche ojos'}
    return {'image': choice(images_people)}