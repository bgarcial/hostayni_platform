from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save


class SliderQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True).filter(start_date__lte=timezone.now()).filter(end_date__gte=timezone.now())


class SliderManager(models.Manager):
    def get_queryset(self):
        return SliderQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    # Return all sliders featured with start_date and end_date and active
    def all_featured(self):
        return self.get_queryset().active().featured()

    def get_featured_item(self):
        try:
            return self.get_queryset().active().featured()[0]
        except:
            return None


def slider_upload(instance, filename):
    return "images/marketing/slider/%s" %(filename)
    # return "images/marketing/slider/%s/%s" %(instance.id, filename)


class Slider(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=120, verbose_name="Ingrese el nombre de quien pauta")
    slug = models.SlugField(max_length=100, blank=True,)
    image = models.ImageField(upload_to=slider_upload, verbose_name="Imagen a aparecer en el carrusel")
    # image = models.FileField(upload_to=slider_upload)

    order = models.IntegerField(default=0, verbose_name="Ingrese el orden en que desea que aparezca la imagen",
                                help_text="Ingrese un numero")

    url_link = models.CharField(max_length=250, null=True, blank=True,
                                verbose_name="Ingrese un enlace promocional", help_text="Opcional")

    header_text = models.CharField(max_length=120, null=True, blank=True,
                                   verbose_name="Ingrese un encabezado para el banner", help_text="Opcional")

    text = models.CharField(max_length=120, null=True, blank=True,
                            verbose_name="Ingrese un caption para el banner", help_text="Opcional")

    active = models.BooleanField(default=False, help_text="Indica si el anuncio estara activo o no en la pagina de inicio en hostayni")

    featured = models.BooleanField(default=False,)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True,
                                  verbose_name="Fecha de inicio del anuncio",
                                  help_text="Indica desde que fecha el anuncio empezara a aparecer en la pagina de inicio de hostayni")
    end_date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True,
                                verbose_name="Fecha de finalizacion del anuncio",
                                help_text="Indica hasta que fecha el anuncio estara en la pagina de inicio de hostayni"
                                )

    objects = SliderManager()

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ['order', '-start_date', '-end_date']

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Slider.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_home_slider_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_home_slider_receiver, sender=Slider)