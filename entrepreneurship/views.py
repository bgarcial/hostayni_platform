from __future__ import unicode_literals

from django.http import Http404, HttpResponseNotModified
from django.shortcuts import render, redirect
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from .models import EntrepreneurshipOffer, EntrepreneurshipOfferImage
from .forms import EntrepreneurshipOfferForm, EntrepreneurshipOfferImagesForm
from hostayni.mixins import UserProfileDataMixin





# Create your views here.


class EntrepreneurshipOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = EntrepreneurshipOffer
    form_class = EntrepreneurshipOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(EntrepreneurshipOfferCreateView, self).form_valid(form)


class EntrepreneurshipOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = EntrepreneurshipOffer
    template_name = 'entrepreneurship/detail.html'
    # context_object_name = 'entrepreneurshipdetail'

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Capturamos quien creo la oferta, y su titulo de anuncio

        offer_owner = self.get_object().created_by.get_long_name()

        offer_owner_company = self.get_object().created_by.get_enterprise_name

        offer_owner_username = self.get_object().created_by.username

        offer_owner_email = self.get_object().created_by.email

        offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email

        interested_username = user.username

        interested_full_name = user.get_long_name()




        offer_url = self.request.get_full_path
        print(offer_url)

        # We get the images of LodgingOffer - LodgingOfferImages model
        entrepreneurship_offer = EntrepreneurshipOffer.objects.get(slug=self.kwargs.get('slug'))
        # We get images via related_name of lodging_offer pk in LodgingOfferImage model
        uploaded = entrepreneurship_offer.entrepreneurshipofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        context['offer_owner_username'] = offer_owner_username
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        # context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context


class EntrepreneurshipOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = EntrepreneurshipOffer
    form_class = EntrepreneurshipOfferForm
    success_message = "Oferta de emprendimiento actualizada con éxito"
    # template_name = 'entrepreneruship/delete.html'

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferUpdateView, self).get_context_data(**kwargs)
        # user = self.request.user
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EntrepreneurshipOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class EntrepreneurshipOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = EntrepreneurshipOffer

    success_url = reverse_lazy("articles:article_list")
    # context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de alojamiento eliminada con éxito"

    """
    def get_success_url(self):
        entrepreneurship_offer = self.get_object()
        #print(entrepreneurship_offer)
        return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
    """

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EntrepreneurshipOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferDeleteView, self).get_context_data(**kwargs)
        return context


def entrepreneurship_offers_by_user(request, username):
    user = request.user
    profile = user.profile
    entrepreneurship_offers = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)

    return render(
        request,
        'entrepreneurship/my_entrepreneurship_offer_list.html',
        {'entrepreneurship_offers': entrepreneurship_offers,
        'userprofile': profile}
    )


class EntrepreneurshipOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'entrepreneurship/my_entrepreneurship_offer_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        entrepreneurship_offers = EntrepreneurshipOffer.objects.filter(created_by__username=user.username)
        context['offers_by_user'] = entrepreneurship_offers

        #if user.is_authenticated():
        #    context['userprofile'] = user.profile
        return context



@login_required
def add_entrepreneurship_offer_images(request, slug):
    user = request.user
    profile = user.profile

    # We get the entrepreneurship offer
    entrep_offer = EntrepreneurshipOffer.objects.get(slug=slug)

    # Verifying user owner offer to edit capabilities
    if entrep_offer.created_by != request.user:
        raise Http404

    # Use the LodgingOfferImageForm
    form_class = EntrepreneurshipOfferImagesForm

    # If we make submit
    if request.method == 'POST':
        # We get data from the submitted form
        form = form_class(data=request.POST, files=request.FILES, instance=entrep_offer)
        if form.is_valid():
            # Create the new LodgingOfferImage object from the submitted form
            EntrepreneurshipOfferImage.objects.create(
                entrepreneurship_offer=entrep_offer, image=form.cleaned_data['image']
            )
            messages.success(request, "La fotografía ha sido cargada y asociada a tu oferta " + entrep_offer.ad_title)
            return redirect('offer:edit_entrepreneurship_images', slug=entrep_offer.slug)
    # Otherwise, just create the lodging offer upload image form
    else:
        form = form_class(instance=entrep_offer)

    # We get all images of a LodginOffer object
    uploads = entrep_offer.entrepreneurshipofferimage.all()

    # Render to template
    return render(request, 'edit_entrepreneurship_offer_images.html', {
        'entrep_offer': entrep_offer,
        'form': form,
        'uploads': uploads,
        'userprofile': profile
    })


class EntrepreneurshipOfferImageUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = EntrepreneurshipOfferImage
    form_class = EntrepreneurshipOfferImagesForm

    # success_url = reverse_lazy("host:edit-study-offer-image", pk_url_kwarg='pk')

    success_message = "Imagen actualizada"

    def get_success_url(self):
        # return reverse("host:edit-study-offer-image", kwargs={self.pk_url_kwarg: self.kwargs.get('pk')})
        return reverse("offer:edit_entrepreneurship_offer_image",
                       kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(EntrepreneurshipOfferImageUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        entrepreneurship_offer_image = EntrepreneurshipOfferImage.objects.get(pk=self.kwargs.get('pk'))
        context['entrepreneurship_offer_image'] = entrepreneurship_offer_image
        return context

    # Permiso para que solo el dueño pueda editarla

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EntrepreneurshipOfferImageUpdateView, self).get_object()
        if not obj.entrepreneurship_offer.created_by == self.request.user:
            raise Http404
        return obj


def contact_owner_offer(request, offer_owner, offer_owner_username, offer_owner_email,
                        interested_full_name, interested_username, interested_email,
                        offer_title, offer_url):
    user = request.user
    if user.is_authenticated:
        # print('Send email')
        mail_subject = 'Interesados en tu oferta'


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

        message = render_to_string('enterpreneurship/contact_user_own_offer.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL,
                  [offer_owner_email, interested_email], html_message=message, fail_silently=True)

        #sleep(60)
        # Hacer esto con celery --- pagina 66 https://docs.google.com/document/d/1aUVRvGFh0MwYZydjXlebaSQJgZnHJDOKx3ccjWmusgc/edit#

        msg_to_owner = render_to_string('enterpreneurship/to_own_offer.html', context)
        send_mail(mail_subject, msg_to_owner, settings.DEFAULT_FROM_EMAIL,
                  [offer_owner_email], html_message=msg_to_owner, fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()
