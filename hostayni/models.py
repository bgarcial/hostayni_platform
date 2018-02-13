from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.conf import settings


class SliderQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True).filter(start_date__lt=timezone.now()).filter(end_date__gte=timezone.now())


class SliderManager(models.Manager):
    def get_queryset(self):
        return SliderQueryset(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
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
    image = models.ImageField(upload_to=slider_upload)
    # image = models.FileField(upload_to=slider_upload)
    order = models.IntegerField(default=0)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = SliderManager()

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['order', '-start_date', '-end_date']

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)





