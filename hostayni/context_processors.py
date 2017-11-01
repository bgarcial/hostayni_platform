# -*- coding: utf-8 -*-

from random import choice

images_people = ['https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia2.jpg','2',
          'https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia3.jpg',
          'https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia4.jpg',
          'https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia-children.jpg',
          'https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/ElZocalo.jpg',
          'https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/israel.jpg',
          ]

def images(request):
    # return {'frase': 'Niche ojos'}
    return {'images': choice(images_people)}