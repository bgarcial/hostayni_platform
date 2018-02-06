# -*- coding: utf-8 -*-

from random import choice

images_people = [
    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia2.jpg',
     'Salar de Uyuni - Bolivia. Cortesía: Juan Jaime Arroyave '),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/Centro_Historico_Lima.jpg',
     'Centro histórico de Lima. Cortesía: Mariana Giraldo'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia3.jpg',
     'Salar de Uyuni - Bolivia. Cortesía: Juan Jaime Arroyave '),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/Arusi-Choco.jpg',
     'Arusí, Chocó. Cortesía: Mariana Giraldo'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia4.jpg',
     'Salar de Uyuni - Bolivia. Cortesía: Juan Jaime Arroyave '),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/Calles_Medellin.jpg',
     'Calles de Medellín. Cortesía: Mariana Giraldo'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/bolivia-children.jpg',
     'Copacabana, Bolivia, Cortesía: Juan Jaime Arroyave'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/Catedral_Manizalez.jpg',
     'Catedral de Manizales. Cortesía: Mariana Giraldo'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/ElZocalo.jpg',
     'El Zocalo - Ciudad de Mexico. Cortesía: Juan Jaime Arroyave'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/La_Candelaria_Bogota.jpg',
     'La Candelaria, Bogotá'),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/israel.jpg',
     'Tzeelim - Israel. Cortesía: Juan Jaime Arroyave',),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/Paracas_Ica_Peru.jpg',
     'Paracas - Ica, Perú. Cortesía: Mariana Giraldo',),

    ('https://s3-sa-east-1.amazonaws.com/ihost-project/assets/img/San_Francisco.jpg',
     'San Francisco, California. Cortesía: Luisa García',)
]

def images(request):
    # return {'frase': 'Niche ojos'}
    return {'image': choice(images_people)}