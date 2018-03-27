from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from entrepreneurship.models import TimeStampModel



# Create your models here.

class AyniOfferManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(AyniOfferManager, self).filter(is_taked=False).filter(is_paid=False).filter(
            created__lte=timezone.now())

    def paid(self, *args, **kwargs):
        return super(AyniOfferManager, self).filter(is_paid=True).filter(created__lte=timezone.now())


def get_ayni_image_path(instance, filename):
    return '/'.join(['daily_life_offer_images', instance.slug, filename])


class AyniOffer(TimeStampModel):

    SOCIAL_PROJECTION = 'Proyección Social'
    ENVIRONMENTAL_PROTECTION = 'Protección del medio ambiente'
    ANIMAL_PROTECTION = 'Protección Animal'

    OFFER_TYPE = (
        (SOCIAL_PROJECTION, "Proyección Social"),
        (ENVIRONMENTAL_PROTECTION,'Protección del medio ambiente'),
        (ANIMAL_PROTECTION, "Protección Animal"),
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

    offer_type = models.CharField(
        max_length=100,
        choices=OFFER_TYPE,
        verbose_name='Tipo de oferta',
    )

    photo = models.ImageField(
        upload_to=get_ayni_image_path,
        blank=False,
        verbose_name='Fotografía',
        null=False,
        help_text='Esta imagen acompañará tu oferta en los resultados de búsquedas'
    )

    address = models.CharField(_("Dirección"), max_length=128, help_text='Precio en pesos colombianos')

    maximum_quota = models.PositiveSmallIntegerField(
        verbose_name='Cupos'
    )

    price = models.CharField(_("Precio"), max_length=128, help_text='Precio en pesos colombianos')

    additional_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción adicional'
    )


    # Este campo sera grabado solo una vez cuando se cree la oferta
    # created = models.DateTimeField( auto_now=False, auto_now_add=True)

    # Cada vez que se grabe en la base de datos se actualice el campo updated
    # modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    is_taked = models.BooleanField(
        _('Oferta tomada'),
        default=False,
    )

    is_paid = models.BooleanField(
        _('Oferta promovida'),
        default=False,
    )

    objects = AyniOfferManager()

    def __str__(self):
        return "%s" % self.ad_title

    def get_absolute_url(self):
        return reverse('ayni_offer:detail', kwargs={'slug': self.slug})

    def get_price(self):
        return self.price

    class Meta:
        ordering = ['-is_paid', '-created', '-modified', ]

    def save(self, *args, **kwargs):
        super(AyniOffer, self).save(*args, **kwargs)

        if self.photo:
            AyniOfferImage.objects.create(
                daily_life_offer=self,
                image=self.photo
            )


def create_slug(instance, new_slug=None):
    slug = slugify(instance.ad_title)
    if new_slug is not None:
        slug = new_slug
    qs = AyniOffer.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_ayni_offer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_ayni_offer_receiver, sender=AyniOffer)


def get_image_filename(instance, filename):
    return '/'.join(['ayni_offer_images', instance.ayni_offer.slug, filename])


class AyniOfferImage(models.Model):
    ayni_offer = models.ForeignKey(AyniOffer, related_name='ayniofferimage')
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Imagen', )

    def __str__(self):
        return self.ayni_offer.ad_title
