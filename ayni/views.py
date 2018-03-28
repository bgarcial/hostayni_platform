from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic import DeleteView, ListView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404, HttpResponseNotModified
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from haystack.query import SearchQuerySet
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from hostayni.mixins import UserProfileDataMixin
from .models import AyniOffer, AyniOfferImage
from .forms import AyniOfferForm, AyniOfferImageForm

# Create your views here.


class AyniOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = AyniOffer
    form_class = AyniOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(AyniOfferCreateView, self).form_valid(form)


class AyniOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = AyniOffer
    template_name = 'ayni/detail.html'
    context_object_name = 'ayni'

    def get_context_data(self, **kwargs):
        context = super(AyniOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Capturamos quien creo la oferta, y su titulo de anuncio

        offer_owner = self.get_object().created_by.get_long_name()

        offer_owner_company = self.get_object().created_by.enterprise_name

        offer_owner_username = self.get_object().created_by.username

        offer_owner_email = self.get_object().created_by.email

        offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email

        interested_username = user.username

        interested_full_name = user.get_long_name()

        offer_url = self.request.get_full_path

        # We get the images of AyniOffer - AyniOfferImages model
        ayni_offer = AyniOffer.objects.get(slug=self.kwargs.get('slug'))

        # We get images via related_name of ayni_offer pk in AyniOfferImage model
        uploaded = ayni_offer.ayniofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        context['offer_owner_username'] = offer_owner_username
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        context['offer_owner_company'] = offer_owner_company
        # context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context


def contact_owner_offer(request, offer_owner, offer_owner_username, offer_owner_email,
                        interested_full_name, interested_username, interested_email,
                        offer_title, offer_url):
    user = request.user
    if user.is_authenticated:
        # print('Send email')
        mail_subject_to_user = 'Has aplicado a una oferta de alojamiento'
        mail_subject_to_owner = 'Interesados en tu oferta'


        context = {
            # usuario dueño de la oferta  TO
            'offer_owner_full_name': offer_owner,
            #'lodging_offer_owner_enterprise_name': lodging_offer_owner_enterprise_name,
            'offer_owner_username': offer_owner_username,
            'offer_owner_email': offer_owner_email,


            # oferta por la que se pregunta
            'offer_title': offer_title,
            'offer_url': offer_url,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            'interested_username': interested_username,
            'interested_email': interested_email,
            'user_interested_full_name': interested_full_name,
        }

        msg_to_who_applies = render_to_string('ayni/message_to_user_who_applies.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject_to_user, msg_to_who_applies, settings.DEFAULT_FROM_EMAIL,
                  [interested_email], html_message=msg_to_who_applies, fail_silently=True)

        #sleep(60)
        # Hacer esto con celery --- pagina 66 https://docs.google.com/document/d/1aUVRvGFh0MwYZydjXlebaSQJgZnHJDOKx3ccjWmusgc/edit#

        msg_to_owner = render_to_string('entrepreneurship/to_own_offer.html', context)
        send_mail(mail_subject_to_owner, msg_to_owner, settings.DEFAULT_FROM_EMAIL,
                  [offer_owner_email], html_message=msg_to_owner, fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()


class AyniOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = AyniOffer
    form_class = AyniOfferForm
    success_message = "Oferta de ayni actualizada con éxito"
    # template_name = 'entrepreneruship/delete.html'

    def get_context_data(self, **kwargs):
        context = super(AyniOfferUpdateView, self).get_context_data(**kwargs)
        # user = self.request.user
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AyniOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class AyniOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = AyniOffer

    success_url = reverse_lazy("articles:article_list")
    # context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de vida diaria eliminada con éxito"

    """
    def get_success_url(self):
        entrepreneurship_offer = self.get_object()
        #print(entrepreneurship_offer)
        return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
    """

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AyniOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class AyniOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'ayni/my_ayni_offers_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = AyniOffer.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(AyniOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        ayni_offers = AyniOffer.objects.filter(created_by__username=user.username)
        context['offers_by_user'] = ayni_offers

        #if user.is_authenticated():
        #    context['userprofile'] = user.profile
        return context


@login_required
def add_ayni_offer_images(request, slug):
    user = request.user
    profile = user.profile

    # We get the ayni_offer
    ayni_offer = AyniOffer.objects.get(slug=slug)

    # Verifying user owner offer to edit capabilities
    if ayni_offer.created_by != request.user:
        raise Http404

    # Use the AyniOfferImageForm
    form_class = AyniOfferImageForm

    # If we make submit
    if request.method == 'POST':
        # We get data from the submitted form
        form = form_class(data=request.POST, files=request.FILES, instance=ayni_offer)
        if form.is_valid():
            # Create the new LodgingOfferImage object from the submitted form
            AyniOfferImage.objects.create(
                ayni_offer=ayni_offer, image=form.cleaned_data['image']
            )
            messages.success(request, "La fotografía ha sido cargada y asociada a tu oferta " + ayni_offer.ad_title)
            return redirect('ayni_offer:edit_images', slug=ayni_offer.slug)
    # Otherwise, just create the lodging offer upload image form
    else:
        form = form_class(instance=ayni_offer)

    # We get all images of a AYNIOffer object
    uploads = ayni_offer.ayniofferimage.all()

    # Render to template
    return render(request, 'edit_ayni_offer_images.html', {
        'ayni_offer': ayni_offer,
        'form': form,
        'uploads': uploads,
        'userprofile': profile
    })


@login_required
def delete_ayni_offer_image(request, id):
    # We get the image
    upload = AyniOfferImage.objects.get(id=id)

    # Security check
    if upload.ayni_offer.created_by != request.user:
        raise Http404

    # Delete image
    upload.delete()
    messages.success(request, 'Tu imágen ha sido borrada, ya no aparecerá en el detalle de tu '
                              'oferta ' + upload.ayni_offer.ad_title)
    # Refresh the edit page
    return redirect('ayni_offer:edit_images', slug=upload.ayni_offer.slug)


class AyniOfferImageUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = AyniOfferImage
    form_class = AyniOfferImageForm

    # success_url = reverse_lazy("host:edit-study-offer-image", pk_url_kwarg='pk')

    success_message = "Imagen actualizada"

    def get_success_url(self):
        # return reverse("host:edit-study-offer-image", kwargs={self.pk_url_kwarg: self.kwargs.get('pk')})
        return reverse("ayni_offer:edit_image",
                       kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(AyniOfferImageUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        ayni_offer_image = AyniOfferImage.objects.get(pk=self.kwargs.get('pk'))
        context['ayni_offer_image'] = ayni_offer_image
        return context

    # Permiso para que solo el dueño pueda editarla

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AyniOfferImageUpdateView, self).get_object()
        if not obj.ayni_offer.created_by == self.request.user:
            raise Http404
        return obj