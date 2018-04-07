from __future__ import unicode_literals
from django.utils import timezone
from haystack import indexes

from .models import EntrepreneurshipOffer


class EntrepreneurshipOfferIndex(indexes.SearchIndex, indexes.Indexable):

    # Cada SearchIndex requiere que uno de sus campos tenga document=True.
    # La convención es llamar a este campo text, y es el campo primario de
    # búsqueda
    # Con use_template=True le estamos diciendo a Haystack que este campo se
    # renderizará a una plantilla de datos para construir el documento que el
    # motor de búsqueda indexará
    text = indexes.CharField(document=True, use_template=True)

    # Tambien indexaremos ad_title to filter searchs by title
    # Con el parámetro model_attr indicamos que este campo
    # corresponde al campo patient del modelo
    ad_title = indexes.CharField(model_attr='ad_title', null=True)

    country = indexes.CharField(model_attr='country', null=True)

    city = indexes.CharField(model_attr='city', null=True)

    offer_type = indexes.CharField(model_attr='offer_type', null=True)

    created = indexes.DateTimeField(model_attr='created')


    # El método get_model()  devuelve el modelo para los documentos que serán
    # almacenados en éste índice.
    def get_model(self, using=None):
        return EntrepreneurshipOffer

    # El metodo inxdex_queryset, retorna el QuerySet para los objetos
    # que serán indexados.
    # Un checkbox para que se deshabilite o habilite la oferta
    # encadenando sete query asi https://stackoverflow.com/questions/34281742/how-to-and-chain-filters-in-a-django-queryset
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created__lte=timezone.now()).filter(is_taked=False)