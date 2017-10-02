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
    HOUSE_APT_SHARE_VISITORS = 'Casa o apartamento para compartir con otros huéspede'
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

    # Fijarle un max_length
    ad_title = models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name='Título de la oferta'
    )

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

    photographies = models.ImageField(
        upload_to='hosting-host-photos',
        blank=False,
        null=False,
        verbose_name='Fotografía'
    )

    room_value = models.CharField(_("Precio"), max_length=128)

    additional_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descripción adicional'
    )

    def __str__(self):
        return "%s" % self.ad_title

    pub_date = models.DateTimeField(
        auto_now_add=True,
    )


    '''
    def get_absolute_url(self):
        return u'/host/lodging-offer/%d' % self.id
    '''
    def get_absolute_url(self):
        return reverse('host:detail', kwargs = {'pk' : self.pk })


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


    '''
    ONE_MONTHS = 'One month or less'
    ONE_TO_SIX_MONTHS = 'One to six months'
    SIX_TO_TWELVE_MONTHS = 'Six to twelve months'
    TWELVE_TO_EIGHTEEN_MONTHS = 'Twelve to eighteen moths'
    EIGHTEEN_TO_TWENTY_FOUR_MONTHS = 'Eighteen to twenty four months'

    TWENTY_FOUR_TO_THIRTY_SIX_MONTHS = 'Twenty four to Thirty six months'
    THIRTY_SIX_TO_FOURTY_EIGHT_MONTHS = 'Thirty six to Fourty eight months'
    FOURTY_EIGHT_TO_SIXTY_MONTHS = 'Fourty eight to Sixty months'
    MORE_THAN_TO_SIXTY_MONTHS = 'More/Greater than Sixty months'

    DURATION_STUDY_CHOICES = (
        (ONE_MONTHS, '1 mes o menos'),
        (ONE_TO_SIX_MONTHS, 'De 1 a 6 meses'),
        (SIX_TO_TWELVE_MONTHS, 'De 6 a 12 meses'),
        (TWELVE_TO_EIGHTEEN_MONTHS, 'De 12 a 18 meses'),
        (EIGHTEEN_TO_TWENTY_FOUR_MONTHS, 'De 18 a 24 meses'),
        (TWENTY_FOUR_TO_THIRTY_SIX_MONTHS, 'De 24 a 36 meses'),
        (THIRTY_SIX_TO_FOURTY_EIGHT_MONTHS, 'De 36 a 48 meses'),
        (FOURTY_EIGHT_TO_SIXTY_MONTHS, 'De 48 a 60 meses'),
        (MORE_THAN_TO_SIXTY_MONTHS, 'Mayor a 60 meses'),

    )
    '''

    CONTINUING_EDUCATION_STUDIES = 'Estudios de educación contínua'
    TECHNIQUE = 'Técnica'
    TECHNOLOGY = 'Tecnología'
    PROFESSIONAL = 'Profesional'
    SPECIALIZATION = 'Especialización'
    MASTER = 'Maestría'
    DOCTORATE = 'Doctorado'
    ACADEMIC_MOBILITY = 'Movilidad académica'

    STUDIES_TYPE_CHOICES = (
        (CONTINUING_EDUCATION_STUDIES, u'Estudios de educación contínua'),
        (TECHNIQUE, u'Tecnología'),
        (TECHNOLOGY, u'Técnica'),
        (PROFESSIONAL, u'Profesional'),
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

    '''
    Model to be removed
    studies_offert_list = ChainedManyToManyField(
        'StudiesOffertList', # Modelo encadenado
        horizontal=False,
        verbose_name='Studies Offert List',
        chained_field='studies_type_offered',
        chained_model_field='studies_type_offered_associated',
        help_text='What are your studies offerts?',
        blank=True,
    )
    '''

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

    studies_value = models.CharField(_("Precio"), max_length=128)

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

    def __str__(self):
        return "{}".format(self.ad_title)

    def get_absolute_url(self):
        return reverse('host:studyoffertdetail', kwargs = {'pk' : self.pk })
    '''
    @property
    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
    '''
