from __future__ import unicode_literals
from django.db import models

from host_information.models import (
    OfferedServices, FeaturesAmenities, RoomInformation,

)

from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from django.db.models.signals import pre_save


'''
class LodgingOfferManager(models.Model):
    use_for_related_fields = True

    #def toggle_contact_own_offer(self, user_interested, user_to_contact, offer):
'''

class LodgingOffer(models.Model):

    ALL_PROPERTY = 'Toda la propiedad'
    PRIVATE_ROOM = 'Habitación privada'
    SHARED_ROOM = 'Habitación compartida'

    ROOM_TYPE_OFFERED_CHOICES = (
        (ALL_PROPERTY, "Toda la propiedad"),
        (PRIVATE_ROOM, "Habitación privada"),
        (SHARED_ROOM, "Habitación compartida"),
    )

    ONE_GUEST = 'Para 1 huésped'
    TWO_GUESTS = 'Para 2 huéspedes'
    THREE_GUESTS = 'Para 3 huéspede'
    FOUR_GUESTS = 'Para 4 huéspedes'
    FIVE_GUESTS = 'Para 5 huéspedes'
    SIX_GUESTS = 'Para 6 huéspedes'
    SEVEN_GUESTS = 'Para 7 huéspedes'
    EIGHT_GUESTS = 'Para 8 huéspedes'
    NINE_GUESTS = 'Para 9 huéspedes'
    TEN_GUESTS = 'Para 10 huéspedes'


    NUMBER_GUESS_ROOM_TYPE_CHOICES = (
        (ONE_GUEST, "Para 1 huésped"),
        (TWO_GUESTS, "Para 2 huéspedes"),
        (THREE_GUESTS, "Para 3 huéspedes"),
        (FOUR_GUESTS, "Para 4 huéspedes"),
        (FIVE_GUESTS, "Para 5 huéspedes"),
        (SIX_GUESTS, "Para 6 huéspedes"),
        (SEVEN_GUESTS, "Para 7 huéspedes"),
        (EIGHT_GUESTS, "Para 8 huéspedes"),
        (NINE_GUESTS, "Para 9 huéspedes"),
        (TEN_GUESTS, "Para 10 huéspedes"),
    )

    HOTEL = 'Hotel'
    HOSTEL = 'Hostal'
    STUDENT_RESIDENCE = 'Residencia estudiantil'
    ACCOMODATION_WITH_LOCAL_FAMILY = 'Acomodación con familia local'
    HOUSE_APT_SHARE_VISITORS = 'Casa o apartamento para compartir con otros huéspedes'
    HOUSE_OR_PRIV_APT = 'Casa o apartamento privado'


    LODGING_OFFER_TYPE_CHOICES = (
        (HOTEL, "Hotel"),
        (HOSTEL, "Hostal"),
        (STUDENT_RESIDENCE, "Residencia estudiantil"),
        (ACCOMODATION_WITH_LOCAL_FAMILY, "Acomodación con familia local"),
        (HOUSE_APT_SHARE_VISITORS, "Casa o apartamento para compartir con otros huéspedes"),
        (HOUSE_OR_PRIV_APT, "Casa o apartamento privado"),
    )

    ONE_STAR = '1 estrella'
    TWO_STARS = '2 estrellas'
    THREE_STARS = '3 estrellas'
    FOUR_STARS = '4 estrellas'
    FIVE_STARS = '5 estrellas'


    STARS_NUMBER_CHOICES = (
        (ONE_STAR, "1 estrella"),
        (TWO_STARS, "2 estrellas"),
        (THREE_STARS, "3 estrellas"),
        (FOUR_STARS, "4 estrellas"),
        (FIVE_STARS, "5 estrellas"),
    )

    SINGLE_BED = 'Cama individual'
    DOUBLE_BED = 'Cama doble'

    BED_TYPE_OFFERED_CHOICES = (
        (SINGLE_BED, "Cama individual"),
        (DOUBLE_BED, "Cama doble"),
    )

    PRIVATE_BATHROOM = 'Baño privado'
    SHARED_BATHROOM = 'Baño compartid'

    BATHROOM_CHOICES = (
        (PRIVATE_BATHROOM, "Baño privado"),
        (SHARED_BATHROOM, "Baño compartido"),
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ad_title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Título de la oferta'
    )

    slug = models.SlugField(max_length=100, blank=True)

    country = CountryField(blank_label='(Seleccionar país)', verbose_name='Pais')

    city = models.CharField(
        max_length=255,
        blank = False,
        verbose_name='Ciudad'
    )
    # Can I use later this package https://github.com/coderholic/django-cities

    address = models.CharField(_("Dirección"), max_length=255)

    latitude = models.CharField(_("latitude"), max_length=255, null=True, blank=True)

    longitude = models.CharField(_("longitude"), max_length=255, null=True, blank=True)

    lodging_offer_type = models.CharField(
        max_length=255,
        choices=LODGING_OFFER_TYPE_CHOICES,
        verbose_name='Tipo de oferta de alojamiento',
    )

    stars = models.CharField(
        max_length=255,
        choices=STARS_NUMBER_CHOICES,
        verbose_name='Número de estrellas',
    )
    '''
    available_dates = models.DateField(
        blank=True,
        null=True,
        verbose_name='Available dates',
        help_text="Days in which is possible bookings",
    )
    
    BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')

    birth_year = models.DateField(
        blank=True,
        null=True,
        verbose_name='Available dates',
        help_text="Days in which is possible bookings",
    )
    '''

    check_in = models.DateField(
        blank=True,
        null=True,
        verbose_name='Check In',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    check_out = models.DateField(
        blank=True,
        null=True,
        verbose_name='Check Out',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    offered_services = models.ManyToManyField(
        OfferedServices,
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
        verbose_name='Servicios ofrecidos',
        related_name="lodgingoffers"
        # here m2m lookup sample
        # https://stackoverflow.com/a/16360605/2773461
    )

    featured_amenities = models.ManyToManyField(
        FeaturesAmenities,
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
        verbose_name='Comodidades destacadas'
    )

    room_type_offered = models.CharField(
        max_length=255,
        choices=ROOM_TYPE_OFFERED_CHOICES,
        verbose_name='Tipo de habitación ofrecida',
    )

    number_guest_room_type = models.CharField(
        max_length=255,
        choices=NUMBER_GUESS_ROOM_TYPE_CHOICES,
        verbose_name='Número de huéspedes en habitación',
    )

    bed_type = models.CharField(
        max_length=20,
        choices=BED_TYPE_OFFERED_CHOICES,
        verbose_name='Tipo de cama',
    )

    bathroom = models.CharField(
        max_length=20,
        choices=BATHROOM_CHOICES,
        verbose_name='Baño',
    )

    room_information = models.ManyToManyField(
        RoomInformation,
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
        verbose_name='Características de la habitación',
        related_name="lodgingoffers"
    )

    image = models.ImageField(
        upload_to='hosting-host-photos',
        blank=False,
        null=False,
        verbose_name='Fotografía'
    )

    room_value = models.CharField(_("Precio"), max_length=128, help_text='Precio en pesos colombianos')

    additional_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descripción adicional'
    )



    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    is_taked = models.BooleanField(
        _('Oferta tomada'),
        default=False,
        help_text=_(
            'Indica si esta oferta ya fue tomada por un usuario.  <br /> Este campo es solo para uso de '
            'actualización de una oferta cuando ya ha habido un acuerdo por ella. '
            'Si se selecciona, no aparecerá en los resultados '
            'de búsquedas. <br /> Des-seleccionéla en lugar de eliminar la oferta'
        ),
    )

    def __str__(self):
        return "%s" % self.ad_title

    '''
    def get_absolute_url(self):
        return u'/host/lodging-offer/%d' % self.id
    '''
    def get_absolute_url(self):
        return reverse('host:detail', kwargs = {'slug' : self.slug })

    def get_price(self):
        return self.room_value


def create_slug(instance, new_slug=None):
    slug = slugify(instance.ad_title)
    if new_slug is not None:
        slug = new_slug
    qs = LodgingOffer.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_lodging_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_lodging_offer_receiver, sender=LodgingOffer)


# class LodgingOfferImage(models.Model):

class StudiesOffert(models.Model):

    ACADEMIC_SEMESTER = 'Semestre académico'
    RESEARCH = 'Investigación'
    ROTATIONS_OR_PRACTICES = 'Rotaciones o prácticas'
    SUMMER_SCHOOL = 'Escuela de verano'

    ACADEMIC_MOBILITY_PROGRAMS_CHOICES = (
        (ACADEMIC_SEMESTER, 'Semestre académico'),
        (RESEARCH, 'Investigación'),
        (ROTATIONS_OR_PRACTICES, 'Rotaciones o prácticas'),
        (SUMMER_SCHOOL, 'Escuela de verano'),
    )


    PRIVATE = 'Privada'
    PUBLIC = 'Pública'
    MIXED = 'Privada - Pública'

    CHARACTER_INSTITUTE_CHOICES = (
        (PRIVATE, "Privada"),
        (PUBLIC, "Pública"),
        (MIXED, "Privada - Pública"),
    )


    CONTINUING_EDUCATION_STUDIES = 'Estudios de educación contínua'
    TECHNIQUE = 'Técnica'
    TECHNOLOGY = 'Tecnología'
    PREGRADO = 'Pregrado'
    SPECIALIZATION = 'Especialización'
    MASTER = 'Maestría'
    DOCTORATE = 'Doctorado'
    ACADEMIC_MOBILITY = 'Movilidad académica'

    STUDIES_TYPE_CHOICES = (
        (CONTINUING_EDUCATION_STUDIES, u'Estudios de educación contínua'),
        (TECHNIQUE, u'Técnica'),
        (TECHNOLOGY, u'Tecnología'),
        (PREGRADO, u'Pregrado'),
        (SPECIALIZATION, u'Especialización'),
        (MASTER, u'Maestría'),
        (DOCTORATE, u'Doctorado'),
        (ACADEMIC_MOBILITY, u'Movilidad académica'),
    )

    VIRTUAL = 'Virtual'
    ON_SITE = 'Presencial'


    MODALITY_CHOICES = (
        (VIRTUAL, "Virtual"),
        (ON_SITE, "Presencial"),

    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ad_title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Título de la oferta'
    )

    slug = models.SlugField(max_length=100, blank=True)

    country = CountryField(blank_label='(Seleccionar país)', verbose_name='País')

    city = models.CharField(
        max_length=255,
        blank = False,
        verbose_name='Ciudad'
    )
    # Can I use later this package https://github.com/coderholic/django-cities

    address = models.CharField(_("Dirección"), max_length=255)

    latitude = models.CharField(_("latitude"), max_length=255, null=True, blank=True)
    longitude = models.CharField(_("longitude"), max_length=255, null=True, blank=True)

    '''
    accreditations = models.ManyToManyField(
        Accreditations,
        verbose_name=u'High Quality accreditations',
        related_name="studiesofferts"
    )
    '''

    institute_character = models.CharField(
        max_length=20,
        choices=CHARACTER_INSTITUTE_CHOICES,
        verbose_name='Caracter de la institución',
    )

    maximum_quota = models.PositiveSmallIntegerField(
        verbose_name='Cupo máximo de estudiantes'
    )

    knowledge_topics = TaggableManager(
        verbose_name="Tópicos de conocimiento",
        help_text=_("Una lista de temáticas separada por comas.")
    )


    studies_type_offered = models.CharField(
        max_length=255,
        choices=STUDIES_TYPE_CHOICES,
        verbose_name='Tipo de estudios ofertados',
    )

    academic_mobility_programs = models.CharField(
        max_length=255,
        choices=ACADEMIC_MOBILITY_PROGRAMS_CHOICES,
        verbose_name='Programas de movilidad académica',
        # help_text='Available student academic mobility programs',
    )

    duration = models.CharField(
        max_length=255,
        verbose_name='Duración',
    )

    modality = models.CharField(
        max_length=20,
        choices=MODALITY_CHOICES,
        verbose_name='Modalidad',
    )

    studies_value = models.CharField(_("Precio"), max_length=128, help_text='Precio en pesos colombianos')

    additional_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descripción adicional',

    )

    # TO-DO Consultar las becas del usuario studyhost solamente

    photo = models.ImageField(
        upload_to='study-host-offert-photos',
        blank=False,
        verbose_name='Fotografía',
        null=False
    )

    pub_date = models.DateTimeField(
        auto_now=True,
        # related_name="lodgingoffers"
    )

    is_taked = models.BooleanField(
        _('Oferta tomada'),
        default=False,
        help_text=_(
            'Indica si esta oferta ya fue tomada por un usuario.  <br /> Este campo es solo para uso de '
            'actualización de una oferta cuando ya ha habido un acuerdo por ella. '
            'Si se selecciona, no aparecerá en los resultados '
            'de búsquedas. <br /> Des-seleccionéla en lugar de eliminar la oferta'
        ),
    )

    def __str__(self):
        return "{}".format(self.ad_title)

    '''
    def get_absolute_url(self):
        return reverse('host:studyoffertdetail', kwargs = {'pk' : self.pk })
    '''

    def get_absolute_url(self):
        return reverse('host:studyoffertdetail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.studies_value


def create_study_offer_slug(instance, new_slug=None):
    slug = slugify(instance.ad_title)
    if new_slug is not None:
        slug = new_slug
    qs = StudiesOffert.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_study_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_study_offer_slug(instance)


pre_save.connect(pre_save_study_offer_receiver, sender=StudiesOffert)
