from django.db import models
from django.conf import settings
from django.utils import timezone


class LodgingOfferCarouselQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True).filter(start_date__lt=timezone.now()).filter(end_date__gte=timezone.now())


class LodgingOfferCarouselManager(models.Manager):
    def get_queryset(self):
        return LodgingOfferCarouselQueryset(self.model, using=self._db)

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


def lodging_slider_upload(instance, filename):
    return "images/marketing/lodging_slider/%s" %(filename)
    # return "images/marketing/slider/%s/%s" %(instance.id, filename)


class LodgingOfferCarousel(models.Model):
    image = models.ImageField(upload_to=lodging_slider_upload)
    # image = models.FileField(upload_to=slider_upload)
    order = models.IntegerField(default=0)
    url_link = models.CharField(max_length=250, null=True, blank=True)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = LodgingOfferCarouselManager()

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['order', '-start_date', '-end_date']

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)


class EducationalOfferSliderQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True).filter(start_date__lt=timezone.now()).filter(end_date__gte=timezone.now())


class EducationalOfferSliderManager(models.Manager):
    def get_queryset(self):
        return EducationalOfferSliderQueryset(self.model, using=self._db)

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


def educational_slider_upload(instance, filename):
    return "images/marketing/educational_slider/%s" %(filename)


class EducationalOfferSlider(models.Model):
    image = models.ImageField(upload_to=educational_slider_upload)
    order = models.IntegerField(default=0)
    url_link = models.CharField(max_length=250, null=True, blank=True)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    start_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = EducationalOfferSliderManager()

    def __str__(self):
        return str(self.image)

    class Meta:
        ordering = ['order', '-start_date', '-end_date']

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)