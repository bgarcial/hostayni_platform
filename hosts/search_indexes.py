import datetime
from django.utils import timezone
from haystack import indexes
from .models import LodgingOffer, StudiesOffert

class StudiesOffertIndex(indexes.SearchIndex, indexes.Indexable):

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

    institute_character = indexes.CharField(model_attr='institute_character', null=True)

    # accreditations = indexes.MultiValueField()

    # Mirar como mejorar este indice de busqueda. Supeditado a las palabras exactas del select.
    maximum_quota = indexes.CharField(model_attr='maximum_quota', null=True)

    studies_type_offered = indexes.MultiValueField()


    # knowledge_topics = indexes.MultiValueField()

    academic_mobility_programs = indexes.CharField(model_attr='academic_mobility_programs', null=True)

    duration = indexes.CharField(model_attr='duration', null=True)

    modality = indexes.CharField(model_attr='modality', null=True)

    pub_date = indexes.DateTimeField(model_attr='pub_date')


    def prepare_studies(self, object):
        return [studies.name for studies in object.studies_type_offered.
            set_all()]


    # El método get_model()  devuelve el modelo para los documentos que serán
    # almacenados en éste índice.
    def get_model(self, using=None):
        return StudiesOffert

    # El metodo inxdex_queryset, retorna el QuerySet para los objetos
    # que serán indexados.
    # Podemos personalizar este query para que se retornen solo
    # las ofertas de alojamiento no tomadas.
    # Un checkbox para que se deshabilite o habilite la oferta
    # encadenando sete query asi https://stackoverflow.com/questions/34281742/how-to-and-chain-filters-in-a-django-queryset
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(pub_date__lte=timezone.now())



class LodgingOfferIndex(indexes.SearchIndex, indexes.Indexable):

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

    address = indexes.CharField(model_attr='address', null=True)

    room_type_offered = indexes.CharField(model_attr='room_type_offered', null=True)

    lodging_offer_type = indexes.CharField(model_attr='lodging_offer_type', null=True)

    number_guest_room_type = indexes.CharField(model_attr='number_guest_room_type', null=True)

    room_value = indexes.CharField(model_attr='room_value', null=True)

    # offered_services = indexes.MultiValueField(model_attr='offered_services__lodgingserviceoffer__name', boost=1.25)

    offered_services = indexes.MultiValueField()

    room_information = indexes.MultiValueField()

    stars = indexes.CharField(model_attr='stars', null=True)

    featured_amenities = indexes.MultiValueField()

    bed_type = indexes.CharField(model_attr='bed_type', null=True)

    bathroom = indexes.CharField(model_attr='bathroom', null=True)

    pub_date = indexes.DateTimeField(model_attr='pub_date')


    def prepare_services(self, object):
        return [services.name for services in object.offered_services.set_all()]

    def prepare_room_caracteristics(self, object):
        return [caracteristics.name for caracteristics in object.room_information.set_all()]

    def prepare_amenities(self, object):
        return [amenities.name for amenities in object.featured_amenities.set_all()]


    # El método get_model()  devuelve el modelo para los documentos que serán
    # almacenados en éste índice.
    def get_model(self, using=None):
        return LodgingOffer

    # El metodo inxdex_queryset, retorna el QuerySet para los objetos
    # que serán indexados.
    # Podemos personalizar este query para que se retornen solo
    # las ofertas de alojamiento no tomadas.
    def index_queryset(self, using=None):
        # return self.LodgingOffer.objects.all()
        return self.get_model().objects.filter(pub_date__lte=timezone.now())


