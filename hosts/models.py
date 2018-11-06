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
from django.utils import timezone


# Resizing the image offers
class LodgingOfferManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(LodgingOfferManager, self).filter(is_taked=False).filter(is_paid=False).filter(
            pub_date__lte=timezone.now())

    def paid(self, *args, **kwargs):
        return super(LodgingOfferManager, self).filter(is_paid=True).filter(pub_date__lte=timezone.now())


def get_lodging_image_search_path(instance, filename):
    return '/'.join(['lodging_offer_images', instance.slug, filename])


class LodgingOffer(models.Model):

    PRIVATE_ROOM = 'Privada'
    SHARED_ROOM = 'Compartida'

    ROOM_TYPE_OFFERED_CHOICES = (

        (PRIVATE_ROOM, "Privada"),
        (SHARED_ROOM, "Compartida"),
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
        blank=False,
        verbose_name='Ciudad'
    )
    # Can I use later this package https://github.com/coderholic/django-cities

    address = models.CharField(_("Dirección"), max_length=255)

    latitude = models.CharField(_("latitude"), max_length=255, null=True, blank=True)

    longitude = models.CharField(_("longitude"), max_length=255, null=True, blank=True)

    check_in = models.DateField(
        blank=True,
        null=True,
        verbose_name='Disponibilidad desde:',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    check_out = models.DateField(
        blank=True,
        null=True,
        verbose_name='Disponibilidad hasta:',
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
        verbose_name='Número de huéspedes en habitación',
    )

    discounts = models.CharField(
        max_length=20,
        verbose_name='Descuentos',
    )

    room_information = models.ManyToManyField(
        RoomInformation,
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
        verbose_name='Características de la habitación',
        related_name="lodgingoffers"
    )

    photo = models.ImageField(
        upload_to=get_lodging_image_search_path,
        blank=False,
        verbose_name='Fotografía',
        null=False,
        help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas'
    )

    location_zone = models.CharField(_("Zona/Barrio"),
                    max_length=128, help_text='Sector por donde está ubicada la oferta')

    monthly_price = models.CharField(_("Precio mensual"), max_length=128,
                                     help_text='Precio en pesos colombianos',
                                     null=True,
                                     blank=True,
                                     )

    room_night_value = models.CharField(_("Precio por noche"), max_length=128,
                                        help_text='Precio en pesos colombianos',
                                        null=True,
                                        blank=True,
                                        )

    additional_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción adicional'
    )

    # Este campo sera grabado solo una vez cuando se cree la oferta
    pub_date = models.DateTimeField(
        auto_now=False, auto_now_add=True
        # related_name="lodgingoffers"
    )

    # Cada vez que se grabe en la base de datos se actualice el campo updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    is_taked = models.BooleanField(
        _('Oferta tomada'),
        default=False,


        # help_text=_(
        #    'Indica si esta oferta ya fue tomada por un usuario.  <br /> Este campo es solo para uso de '
        #    'actualización de una oferta cuando ya ha habido un acuerdo por ella. '
        #    'Si se selecciona, no aparecerá en los resultados '
        #    'de búsquedas. <br /> Des-seleccionéla en lugar de eliminar la oferta'
        # ),
    )

    is_paid = models.BooleanField(
        _('Oferta promovida'),
        default=False,
    )

    objects = LodgingOfferManager()

    def __str__(self):
        return "%s" % self.ad_title

    '''
    def get_absolute_url(self):
        return u'/host/lodging-offer/%d' % self.id
    '''

    def get_absolute_url(self):
        return reverse('host:detail', kwargs={'slug': self.slug})

    def get_monthly_price(self):
        return self.monthly_price

    def get_room_night_value(self):
        return self.room_night_value

    class Meta:
        ordering = ['-is_paid', '-pub_date', '-updated', ]

    def save(self, *args, **kwargs):
        super(LodgingOffer, self).save(*args, **kwargs)

        if self.photo:
            LodgingOfferImage.objects.create(
                lodging_offer=self,
                image=self.photo
            )


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


def get_image_filename(instance, filename):
    # title = instance.lodging_offer.ad_title
    # slug = slugify(title)
    # return "lodging_offer_images/%s/%s" % (slug, filename)
    return '/'.join(['lodging_offer_images', instance.lodging_offer.slug, filename])


class LodgingOfferImage(models.Model):
    lodging_offer = models.ForeignKey(LodgingOffer, related_name='lodgingofferimage')
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Imagen', )

    '''
    def save(self, *args, **kwargs):
        super(LodgingOfferImage, self).save(*args, **kwargs)

        # We check to make sure an image exists
        if self.image:
            thumbnail_image = Image.open(self.image)
            # Open image and check their size
            i_width, i_height = thumbnail_image.size
            max_size=(1000,1000)

            image_types = {
                'jpg': 'JPEG',
                'png': 'PNG',
                'gif': 'GIF',
                'tif': 'TIFF',
            }

            # We resize the image if it's too large
            if i_width > 1000:
                buffer = BytesIO()

                thumbnail_image = Image.open(self.image,)
                thumbnail_image.thumbnail(max_size, Image.ANTIALIAS)

                filename_suffix = Path(self.image.file).name[1:]
                print(filename_suffix)
                image_format = image_types[filename_suffix]

                thumbnail_image.save(buffer, format=image_format)

                file_object = File(buffer)
                file_object.content_type = 'image/jpeg'

                self.image.save(self.image.file, file_object)
                self.save()
    '''

    def __str__(self):
        return self.lodging_offer.ad_title


def get_image_search_path(instance, filename):
    return '/'.join(['educational_offer_images', instance.slug, filename])


def get_image_supporters_search_path(instance, filename):
    return '/'.join(['educational_offer_images/supporters', instance.slug, filename])

class StudiesOffertManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(StudiesOffertManager, self).filter(finished=False).filter(is_paid=False).filter(
            pub_date__lte=timezone.now())

    def paid(self, *args, **kwargs):
        return super(StudiesOffertManager, self).filter(is_paid=True).filter(pub_date__lte=timezone.now())


class StudiesOffert(models.Model):

    SHORT_COURSE = 'Curso corto'
    SEMINAR = 'Seminario'
    DIPLOMAT = 'Diplomado'
    WORKSHOP = 'Taller'
    TECHNIQUE = 'Técnica'

    FORMATION_TYPE_CHOICES = (
        (SHORT_COURSE, u'Curso corto'),
        (SEMINAR, u'Seminario'),
        (DIPLOMAT, u'Diplomado'),
        (WORKSHOP, u'Taller'),
        (TECHNIQUE, u'Técnica'),
    )

    VIRTUAL = 'Virtual'
    ON_SITE = 'Presencial'
    SEMI_ON_SITE = 'Semi-presencial'

    MODALITY_CHOICES = (
        (VIRTUAL, "Virtual"),
        (ON_SITE, "Presencial"),
        (SEMI_ON_SITE, "Semi-presencial"),

    )

    SPACE_AVAILABLE = 'Cupos disponibles'
    SOLD_OUT_SPACES_ = 'Cupos agotados'
    CANCELLED = 'Cancelada'

    STATUS_CHOICES = (
        (SPACE_AVAILABLE, u'Cupos disponibles'),
        (SOLD_OUT_SPACES_, u'Cupos agotados'),
        (CANCELLED, u'Cancelada'),
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
        blank=False,
        verbose_name='Ciudad'
    )
    # Can I use later this package https://github.com/coderholic/django-cities

    address = models.CharField(_("Dirección"), max_length=255)

    latitude = models.CharField(_("latitude"), max_length=255, null=True, blank=True)
    longitude = models.CharField(_("longitude"), max_length=255, null=True, blank=True)

    formation_type_offered = models.CharField(
        max_length=255,
        choices=FORMATION_TYPE_CHOICES,
        verbose_name='Tipo de formación',
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

    place = models.CharField(
        max_length=255,
        verbose_name='Lugar',
    )

    schedule = models.CharField(
        max_length=255,
        verbose_name='Horario',
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de inicio:',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    finish_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de terminación:',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    studies_value = models.CharField(_("Precio"), max_length=128, help_text='Precio en pesos colombianos')

    discounts = models.CharField(_("Descuento"),
                                 max_length=128, help_text='Descuentos')

    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name='Estado',
    )

    organizers = models.ImageField(
        upload_to=get_image_search_path,
        blank=True,
        verbose_name='Organizadores',
        null=True,
        help_text='Logos de los organizadores'
    )

    sponsors = models.ImageField(
        upload_to=get_image_search_path,
        blank=True,
        verbose_name='Patrocinadores',
        null=True,
        help_text='Logos de los patrocinadores'
    )

    support = models.ImageField(
        upload_to=get_image_search_path,
        blank=True,
        verbose_name='Apoya',
        null=True,
        help_text='Logos de quien apoya'
    )

    additional_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción adicional',

    )

    photo = models.ImageField(
        upload_to=get_image_search_path,
        blank=False,
        verbose_name='Fotografía',
        null=False,
        help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas'
    )

    # Este campo sera grabado solo una vez cuando se cree el articulo
    pub_date = models.DateTimeField(
        auto_now=False, auto_now_add=True
        # related_name="lodgingoffers"
    )

    # Cada vez que se grabe en la base de datos se actualice el campo updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    finished = models.BooleanField(
        _('Oferta finalizada'),
        default=False,
    )

    is_paid = models.BooleanField(
        _('Oferta promovida'),
        default=False,
    )

    objects = StudiesOffertManager()

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

    class Meta:
        ordering = ['-is_paid', '-pub_date', '-updated', ]

    def save(self, *args, **kwargs):
        super(StudiesOffert, self).save(*args, **kwargs)

        if self.photo:
            StudyOfferImage.objects.create(
                study_offer=self,
                image=self.photo
            )


def create_study_offer_slug(instance, new_slug=None):
    slug = slugify(instance.ad_title)
    if new_slug is not None:
        slug = new_slug
    qs = StudiesOffert.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_study_offer_slug(instance, new_slug=new_slug)
    return slug


def pre_save_study_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_study_offer_slug(instance)


pre_save.connect(pre_save_study_offer_receiver, sender=StudiesOffert)


def get_image_path(instance, filename):
    return '/'.join(['educational_offer_images', instance.study_offer.slug, filename])


# CROP_SETTINGS = {'size': (1000, 500), 'crop': 'smart'}


class StudyOfferImage(models.Model):
    # puedo poner headere text and small text
    study_offer = models.ForeignKey(StudiesOffert, related_name='uploadsstudyoffer')
    image = models.ImageField(upload_to=get_image_path, verbose_name='Seleccionar imagen')

    # images folder per object

    def __str__(self):
        return self.study_offer.ad_title

    '''
    def get_image_url(self):
        return "%s/%s/%s" %(settings.MEDIA_URL, self.study_offer.slug, self.image)


    def save(self, *args, **kwargs):
        super(UploadStudyOffer, self).save(*args, **kwargs)
        # We first check to make sure an image exists
        if self.image:
            # Open image and check their size
            image = Image.open(self.image)
            i_width, i_height = image.size
            max_size = (1000,1000)

            # We resize the image if it's too large
            if i_width > 1000:
                image.thumbnail(max_size, Image.ANTIALIAS)
                # image.save(self.image.name) #[Errno 2] No such file or directory: 'studyoffer_images/ingenieria-de-sistemas/15061122523583.jpg'
                image.save(self.image.file)
                # image.save(self.image.url)
                # image.save(self.image.path) #This backend doesn't support absolute paths.
    '''