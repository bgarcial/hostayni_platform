from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from django.conf import settings
from django.core.validators import URLValidator

from phonenumber_field.modelfields import PhoneNumberField
# https://github.com/stefanfoulis/django-phonenumber-field

from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


# Create your models here.

class TimeStampModel(models.Model):
    """
    An abstract base class model that provide self-updating
    created and modify fields
    """
    # Este campo sera grabado solo una vez cuando se cree el modelo
    created = models.DateTimeField(auto_now_add=True)

    # Cada vez que se grabe en la base de datos se actualice el campo modified
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EntrepreneurshipOfferManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(EntrepreneurshipOfferManager, self).filter(is_taked=False).filter(is_paid=False).filter(
            created__lte=timezone.now())

    def paid(self, *args, **kwargs):
        return super(EntrepreneurshipOfferManager, self).filter(is_paid=True).filter(created__lte=timezone.now())


def get_entrepreneurship_image_path(instance, filename):
    return '/'.join(['entrepreneurship_offer_images', instance.slug, filename])


class EntrepreneurshipOffer(TimeStampModel):

    TRAINING_MENTORING = 'Formación o Mentorías'
    CALL_FOR_ENTREPRENEURS = 'Convocatoria para emprendedores o empresarios'
    VOLUNTEERS = 'Voluntariados'
    CONFERENCES = 'Conferencias'
    SIMPOSIUMS = 'Simposios'
    NETWORKING = 'Espacios de Networking'

    OFFER_TYPE = (
        (TRAINING_MENTORING, "Formación o Mentorías"),
        (CALL_FOR_ENTREPRENEURS, "Convocatoria para emprendedores o empresarios"),
        (VOLUNTEERS, "Voluntariados"),
        (CONFERENCES, "Conferencias"),
        (SIMPOSIUMS, "Simposios"),
        (NETWORKING, "Espacios de Networking"),
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

    offer_type = models.CharField(
        max_length=100,
        choices=OFFER_TYPE,
        verbose_name='Tipo de oferta',
    )

    price = models.CharField(_("Precio"), max_length=128,
                             help_text='Precio en pesos colombianos',
                             null=True,
                             blank=True
                             )

    country = CountryField(blank_label='(Seleccionar país)', verbose_name='Pais')

    city = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Ciudad'
    )

    date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha del evento o cierre de la convocatoria',
        help_text="Ingresar aquí la fecha del evento o cierre de la convocatoria",
    )

    url = models.TextField(
        validators=[URLValidator()],
        verbose_name='Dirección de enlace',
        help_text='Para mayor información referencie una dirección o enlace web',
        null=True,
        blank=True,
    )

    contact_name = models.CharField(
        max_length=100,
        verbose_name='Nombre de contacto',
        null=True,
        blank=True
    )

    phone_number = PhoneNumberField(
        blank=True,
        help_text="Por favor use el siguiente formato: <em>+Country Code-Number</em>.",
        verbose_name='Número telefónico de contacto',
        null = True,
    )

    email = models.CharField(
        max_length=100,
        verbose_name='Correo electrónico de contacto',
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to=get_entrepreneurship_image_path,
        blank=False,
        verbose_name='Fotografía',
        null=False,
        help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas'
    )

    # Este campo sera grabado solo una vez cuando se cree la oferta
    # created = models.DateTimeField( auto_now=False, auto_now_add=True)

    # Cada vez que se grabe en la base de datos se actualice el campo updated
    # modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    additional_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción adicional'
    )

    is_taked = models.BooleanField(
        _('Oferta tomada'),
        default=False,
    )

    is_paid = models.BooleanField(
        _('Oferta promovida'),
        default=False,
    )

    objects = EntrepreneurshipOfferManager()

    def __str__(self):
        return "%s" % self.ad_title

    def get_absolute_url(self):
        return reverse('offer:detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.price

    class Meta:
        ordering = ['-is_paid', '-created', '-modified', ]

    def save(self, *args, **kwargs):
        super(EntrepreneurshipOffer, self).save(*args, **kwargs)

        if self.photo:
            EntrepreneurshipOfferImage.objects.create(
                entrepreneurship_offer=self,
                image=self.photo
            )



def create_slug(instance, new_slug=None):
    slug = slugify(instance.ad_title)
    if new_slug is not None:
        slug = new_slug
    qs = EntrepreneurshipOffer.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_entrepreneurship_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_entrepreneurship_offer_receiver, sender=EntrepreneurshipOffer)


def get_image_filename(instance, filename):
    return '/'.join(['entrepreneurship_offer_images', instance.entrepreneurship_offer.slug, filename])


class EntrepreneurshipOfferImage(models.Model):
    entrepreneurship_offer = models.ForeignKey(EntrepreneurshipOffer, related_name='entrepreneurshipofferimage')
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Imagen', )

    def __str__(self):
        return self.entrepreneurship_offer.ad_title
