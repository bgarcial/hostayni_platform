from __future__ import unicode_literals
from django.shortcuts import render, redirect

from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404, HttpResponseNotModified
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from haystack.query import SearchQuerySet
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from hostayni.mixins import UserProfileDataMixin
from .models import DailyLifeOffer, DailyLifeOfferImage
from .forms import DailyLifeOfferForm, DailyLifeOfferImagesForm, DailyLifeOfferSearchForm
from carousel_offers.models import DailyLifeOfferCarousel


# Create your views here.

class DailyLifeOfferSearch(FormView):
    template_name = 'daily_life/daily_life_offer_search.html'

    # first we instantiate the SearchForm that we created before.
    form_class = DailyLifeOfferSearchForm()

    def get(self, request, *args, **kwargs):
        # We are going to submit the form using the GET method so that the
        # resulting URL includes the query parameter.
        form = DailyLifeOfferSearchForm(self.request.GET or None)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferSearch, self).get_context_data(**kwargs)
        user = self.request.user
        form = DailyLifeOfferSearchForm(self.request.GET or None)

        # When the form is submitted, we instantiate it with the submitted GET
        # data and we check that the given data is valid. If the form is
        # valid, we use the we use SearchQuerySet to perform a search for
        # indexed LodgingOffer objects whose main content contains the given
        # query

        qs = DailyLifeOffer.objects.active()
        context['offer_list'] = qs

        qs_paid = DailyLifeOffer.objects.paid()
        context['offers_paid'] = qs_paid

        sliders = DailyLifeOfferCarousel.objects.all_featured()
        context['sliders'] = sliders

        if form.is_valid():
            cd = form.cleaned_data
            # The load_all() method loads all related LodgingOffer objects
            # from the database at once
            # With this method, we populate the search results with the
            # database objects to avoid per-object access to the database when
            # iterating over results to access object data.
            results = SearchQuerySet().models(DailyLifeOffer)\
                          .filter(content=cd['query']).load_all()

            # Finally, we store the total number of results in a total_results
            # variable and pass the local variables as context to render a
            # template.
            total_results = results.count()
            context.update({
                'cd': cd,
                'results':results,
                'total_results': total_results,

            })
        if user.is_authenticated():
            context['userprofile'] = user.profile

        return context


class DailyLifeOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = DailyLifeOffer
    form_class = DailyLifeOfferForm
    success_message = "Tu oferta de emprendiemiento fue creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.created = timezone.now()
        form.save()
        return super(DailyLifeOfferCreateView, self).form_valid(form)


class DailyLifeOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = DailyLifeOffer
    template_name = 'daily_life/detail.html'
    context_object_name = 'dailylife'

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Capturamos quien creo la oferta, y su titulo de anuncio

        offer_owner = self.get_object().created_by.get_long_name()
        print("Dueño de la oferta", offer_owner)

        # offer_owner_company = self.get_object().created_by.enterprise_name
        # print("Dueño por si es una compania", offer_owner_company)

        # offer_owner_username = self.get_object().created_by.username
        # print("Username del dueño de oferta", offer_owner_username)

        offer_owner_email = self.get_object().created_by.email
        print("Emai dueño oferta", offer_owner_email)

        offer_title = self.get_object().ad_title
        print("Titulo ofeta", offer_title)

        # Capturamos los datos de quien esta interesado en la oferta
        interested_email = user.email
        print(interested_email)

        #interested_username = user.username
        # print(interested_username)

        interested_full_name = user.get_long_name()
        print(interested_full_name)

        offer_url = self.request.get_full_path
        print(offer_url)

        # We get the images of DailyLifeOffer - DailyLifeOfferImages model
        daily_life_offer = DailyLifeOffer.objects.get(slug=self.kwargs.get('slug'))

        # We get images via related_name of lodging_offer pk in LodgingOfferImage model
        uploaded = daily_life_offer.dailylifeofferimage.all()

        # We send the contexts
        context['uploads'] = uploaded
        # context['offer_owner_username'] = offer_owner_username
        context['offer_owner_email'] = offer_owner_email
        context['offer_owner'] = offer_owner
        # context['offer_owner_company'] = offer_owner_company
        # context['offer_owner_company'] = offer_owner_company
        context['offer_title'] = offer_title

        context['interested_email'] = interested_email
        # context['interested_username'] = interested_username
        context['interested_full_name'] = interested_full_name

        context['offer_url'] = offer_url

        return context


def contact_owner_offer(request, offer_owner, offer_owner_email,
                        interested_full_name, interested_email,
                        offer_title, offer_url):
    user = request.user
    if user.is_authenticated:
        # print('Send email')
        mail_subject_to_user = 'Has aplicado a una oferta de vida diaria'
        mail_subject_to_owner = 'Interesados en tu oferta'


        context = {
            # usuario dueño de la oferta  TO
            'offer_owner_full_name': offer_owner,
            #'lodging_offer_owner_enterprise_name': lodging_offer_owner_enterprise_name,
            # 'offer_owner_username': offer_owner_username,
            'offer_owner_email': offer_owner_email,


            # oferta por la que se pregunta
            'offer_title': offer_title,
            'offer_url': offer_url,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            # 'interested_username': interested_username,
            'interested_email': interested_email,
            'user_interested_full_name': interested_full_name,
        }

        msg_to_who_applies = render_to_string('daily_life/message_to_user_who_applies.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject_to_user, msg_to_who_applies, settings.DEFAULT_FROM_EMAIL,
                  [interested_email], html_message=msg_to_who_applies, fail_silently=True)

        #sleep(60)
        # Hacer esto con celery --- pagina 66 https://docs.google.com/document/d/1aUVRvGFh0MwYZydjXlebaSQJgZnHJDOKx3ccjWmusgc/edit#

        msg_to_owner = render_to_string('daily_life/to_own_offer.html', context)
        send_mail(mail_subject_to_owner, msg_to_owner, settings.DEFAULT_FROM_EMAIL,
                  [offer_owner_email], html_message=msg_to_owner, fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()


class DailyLifeOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = DailyLifeOffer
    form_class = DailyLifeOfferForm
    success_message = "Oferta de vida diaria actualizada con éxito"
    # template_name = 'entrepreneruship/delete.html'

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferUpdateView, self).get_context_data(**kwargs)
        # user = self.request.user
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DailyLifeOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class DailyLifeOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = DailyLifeOffer

    success_url = reverse_lazy("articles:article_list")
    # context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de vida diaria eliminada con éxito"

    def get_success_url(self):
        daily_life_offers = self.get_object()
        # print(entrepreneurship_offer)
        # return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
        return reverse_lazy("daily_life_offer:list", kwargs={'username': daily_life_offers.created_by.username})

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DailyLifeOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj



@login_required
def add_daily_life_offer_images(request, slug):
    user = request.user
    profile = user.profile

    # We get the daily_life offer
    daily_life_offer = DailyLifeOffer.objects.get(slug=slug)

    # Verifying user owner offer to edit capabilities
    if daily_life_offer.created_by != request.user:
        raise Http404

    # Use the LodgingOfferImageForm
    form_class = DailyLifeOfferImagesForm

    # If we make submit
    if request.method == 'POST':
        # We get data from the submitted form
        form = form_class(data=request.POST, files=request.FILES, instance=daily_life_offer)
        if form.is_valid():
            # Create the new LodgingOfferImage object from the submitted form
            DailyLifeOfferImage.objects.create(
                daily_life_offer=daily_life_offer, image=form.cleaned_data['image']
            )
            messages.success(request, "La fotografía ha sido cargada y asociada a tu oferta " + daily_life_offer.ad_title)
            return redirect('daily_life_offer:edit_images', slug=daily_life_offer.slug)
    # Otherwise, just create the lodging offer upload image form
    else:
        form = form_class(instance=daily_life_offer)

    # We get all images of a LodginOffer object
    uploads = daily_life_offer.dailylifeofferimage.all()

    # Render to template
    return render(request, 'edit_daily_life_offer_images.html', {
        'daily_life_offer': daily_life_offer,
        'form': form,
        'uploads': uploads,
        'userprofile': profile
    })


class DailyLifeOfferImageUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = DailyLifeOfferImage
    form_class = DailyLifeOfferImagesForm

    # success_url = reverse_lazy("host:edit-study-offer-image", pk_url_kwarg='pk')

    success_message = "Imagen actualizada"

    def get_success_url(self):
        # return reverse("host:edit-study-offer-image", kwargs={self.pk_url_kwarg: self.kwargs.get('pk')})
        return reverse("daily_life_offer:edit_image",
                       kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOfferImageUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        daily_life_offer_image = DailyLifeOfferImage.objects.get(pk=self.kwargs.get('pk'))
        context['daily_life_offer_image'] = daily_life_offer_image
        return context

    # Permiso para que solo el dueño pueda editarla

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(DailyLifeOfferImageUpdateView, self).get_object()
        if not obj.daily_life_offer.created_by == self.request.user:
            raise Http404
        return obj


@login_required
def delete_daily_life_offer_image(request, id):
    # We get the image
    upload = DailyLifeOfferImage.objects.get(id=id)

    # Security check
    if upload.daily_life_offer.created_by != request.user:
        raise Http404

    # Delete image
    upload.delete()
    messages.success(request, 'Tu imágen ha sido borrada, ya no aparecerá en el detalle de tu '
                              'oferta ' + upload.daily_life_offer.ad_title)
    # Refresh the edit page
    return redirect('daily_life_offer:edit_images', slug=upload.daily_life_offer.slug)


class DailyLifeOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'daily_life/my_daily_life_offer_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = DailyLifeOffer.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(DailyLifeOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        # daily_life_offers = DailyLifeOffer.objects.filter(created_by__username=user.username)
        daily_life_offers = DailyLifeOffer.objects.filter(created_by=user)
        context['offers_by_user'] = daily_life_offers

        #if user.is_authenticated():
        #    context['userprofile'] = user.profile
        return context