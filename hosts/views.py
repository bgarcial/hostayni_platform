from __future__ import unicode_literals

from time import sleep

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.forms import modelformset_factory
from django.http import HttpResponseNotModified, HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic import DeleteView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User
from django.contrib.auth.decorators import login_required
from hostayni.mixins import UserProfileDataMixin
from rest_framework import viewsets


from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from .models import LodgingOffer, StudiesOffert, RoomInformation, LodgingOfferImage, StudyOfferImage

from host_information.models import OfferedServices, FeaturesAmenities
from .serializers import LodgingOfferSerializer,StudiesOffertSerializer

from .forms import (LodgingOfferForm, StudiesOffertForm, LodgingOfferSearchForm,
                    StudiesOffertSearchForm, LodgingOfferImagesForm, StudyOfferImagesUploadForm)

from django.views.generic.edit import FormView
from haystack.query import SearchQuerySet
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from carousel_offers.models import LodgingOfferCarousel, EducationalOfferCarousel

# Create your views here.

class LodgingOfferAjax(ListView):
    template_name = 'hosts/retrieve-offers.html'
    queryset = LodgingOffer.objects.all()



# ViewSets define the view behavior.

class LodgingOfferViewSet(viewsets.ModelViewSet):
    # lookup_field = 'name'
    queryset = LodgingOffer.objects.all()
    serializer_class = LodgingOfferSerializer

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LodgingOfferViewSet, self).dispatch(request, *args, **kwargs)
    """


class StudiesOffertViewSet(viewsets.ModelViewSet):
    # lookup_field = 'name'
    queryset = StudiesOffert.objects.all()
    serializer_class = StudiesOffertSerializer


class StudiesOffertSearch(FormView):
    template_name = 'hosts/studiesoffert_search.html'
    form_class = StudiesOffertSearchForm

    def get(self, request, *args, **kwargs):
        # We are going to submit the form using the GET method so that the
        # resulting URL includes the query parameter.
        form = StudiesOffertSearchForm(self.request.GET or None)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(StudiesOffertSearch, self).get_context_data(**kwargs)
        user = self.request.user

        form = StudiesOffertSearchForm(self.request.GET or None)

        qs = StudiesOffert.objects.active()
        context['offer_list'] = qs

        qs_paid = StudiesOffert.objects.paid()
        context['offers_paid'] = qs_paid

        sliders = EducationalOfferCarousel.objects.all_featured()
        context['sliders'] = sliders


        # When the form is submitted, we instantiate it with the submitted GET
        # data and we check that the given data is valid. If the form is
        # valid, we use the we use SearchQuerySet to perform a search for
        # indexed LodgingOffer objects whose main content contains the given
        # query
        if form.is_valid():
            cd = form.cleaned_data
            # The load_all() method loads all related LodgingOffer objects
            # from the database at once
            # With this method, we populate the search results with the
            # database objects to avoid per-object access to the database when
            # iterating over results to access object data.
            results = SearchQuerySet().models(StudiesOffert)\
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


class LodgingOfferSearch(FormView):
    template_name = 'hosts/lodgingoffer_search.html'

    # first we instantiate the SearchForm that we created before.
    form_class = LodgingOfferSearchForm()

    def get(self, request, *args, **kwargs):
        # We are going to submit the form using the GET method so that the
        # resulting URL includes the query parameter.
        form = LodgingOfferSearchForm(self.request.GET or None)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(LodgingOfferSearch, self).get_context_data(**kwargs)
        user = self.request.user
        form = LodgingOfferSearchForm(self.request.GET or None)

        # When the form is submitted, we instantiate it with the submitted GET
        # data and we check that the given data is valid. If the form is
        # valid, we use the we use SearchQuerySet to perform a search for
        # indexed LodgingOffer objects whose main content contains the given
        # query

        qs = LodgingOffer.objects.active()
        context['offer_list'] = qs

        qs_paid = LodgingOffer.objects.paid()
        context['offers_paid'] = qs_paid

        sliders = LodgingOfferCarousel.objects.all_featured()
        context['sliders'] = sliders

        if form.is_valid():
            cd = form.cleaned_data
            # The load_all() method loads all related LodgingOffer objects
            # from the database at once
            # With this method, we populate the search results with the
            # database objects to avoid per-object access to the database when
            # iterating over results to access object data.
            results = SearchQuerySet().models(LodgingOffer)\
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


class StudyOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'hosts/studiesoffer_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = StudiesOffert.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(StudyOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        # studies_offers = StudyOffersByUser.objects.filter(created_by__username=user.username)
        studies_offers = StudiesOffert.objects.filter(created_by=user)
        context['offers_by_user'] = studies_offers
        return context

'''
def studies_offers_by_user(request, username):
    user = request.user
    profile = user.profile
    studies_offers = StudiesOffert.objects.filter(created_by__username=user.username)

    return render(
        request,
        'hosts/studiesoffer_list.html',
        {'studies_offers':studies_offers,
        'userprofile':profile}
    )

'''


class LodgingOffersByUser(LoginRequiredMixin, UserProfileDataMixin, ListView):
    template_name = 'hosts/lodgingoffer_list.html'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset_list = LodgingOffer.objects.filter(created_by__username=user.username)
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(LodgingOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        # lodging_offers = LodgingOffer.objects.filter(created_by__username=user.username)
        lodging_offers = LodgingOffer.objects.filter(created_by=user)
        context['offers_by_user'] = lodging_offers
        return context

'''
def lodging_offers_by_user(request, username):
    user = request.user
    profile = user.profile
    lodging_offers = LodgingOffer.objects.filter(created_by__email=user.email)

    return render(
        request,
        'hosts/lodgingoffer_list.html',
        {'lodging_offers': lodging_offers,
        'userprofile': profile}
    )

'''


class HostingOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = LodgingOffer
    form_class = LodgingOfferForm
    success_message = "Tu oferta de alojamiento creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"



    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.pub_date = timezone.now()
        form.save()
        return super(HostingOfferCreateView, self).form_valid(form)


class HostingOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = LodgingOffer
    form_class = LodgingOfferForm
    #success_url = reverse_lazy("dashboard")
    # success_url = reverse_lazy("hosts:detail-lodging-offer")
    success_message = "Oferta de alojamiento actualizada con éxito"

    def get_context_data(self, **kwargs):
        context = super(HostingOfferUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        #lodging_offer = LodgingOffer.objects.get(slug=self.kwargs.get('slug'))
        #print(lodging_offer)
        #print(user)

        #if not (lodging_offer.created_by_id == user.id):
        #    return HttpResponse("It is not yours ! You are not permitted !",
        #                        content_type="application/json", status=403)
        return context

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(HostingOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class HostingOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = LodgingOffer
    template_name = 'hosts/lodgingoffer_detail.html'
    context_object_name = 'lodgingofferdetail'

    def get_context_data(self, **kwargs):
        context = super(HostingOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # roominformation = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))
        roominformation = LodgingOffer.objects.get(slug=self.kwargs.get('slug'))
        room_information_lodging_offer = roominformation.room_information.all()
        #inf = self.kwargs['room_information_set.all()']

        #room_information = set(queryset.values_list('room_information__name', flat=True).distinct())

        context['lodgingoffer'] = room_information_lodging_offer

        # offeredservices = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))
        offeredservices = LodgingOffer.objects.get(slug=self.kwargs.get('slug'))

        query = offeredservices.offered_services.all()

        context['offeredservices'] = query

        # featuredamenities = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))
        featuredamenities = LodgingOffer.objects.get(slug=self.kwargs.get('slug'))

        fe_amen_query = featuredamenities.featured_amenities.all()
        context['featuredamenities'] = fe_amen_query

        # Capturamos quien creo la oferta, y su titulo de anuncio
        #lodging_offer_owner = self.get_object()
        lodging_offer_owner_full_name = self.get_object().created_by.get_long_name()
        # lodging_offer_owner_enterprise_name = self.get_object().created_by.get_enterprise_name
        lodging_offer_owner_username = self.get_object().created_by.username
        lodging_offer_owner_email = self.get_object().created_by.email
        lodging_offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        user_interested_email = user.email
        user_interested_username = user.username
        user_interested_full_name = user.get_long_name()


        url_offer = self.request.get_full_path

        # We get the images of LodgingOffer - LodgingOfferImages model
        lodging_offer = LodgingOffer.objects.get(slug=self.kwargs.get('slug'))
        # We get images via related_name of lodging_offer pk in LodgingOfferImage model
        uploads = lodging_offer.lodgingofferimage.all()

        # We send the contexts
        context['uploads'] = uploads
        context['lodging_offer_owner_email'] = lodging_offer_owner_email
        context['lodging_offer_owner_username'] = lodging_offer_owner_username
        context['lodging_offer_owner_full_name'] = lodging_offer_owner_full_name
        # context['lodging_offer_owner_enterprise_name'] = lodging_offer_owner_enterprise_name
        context['lodging_offer_title'] = lodging_offer_title

        context['user_interested_email'] = user_interested_email
        context['user_interested_username'] = user_interested_username
        context['user_interested_full_name'] = user_interested_full_name

        context['offer_url'] = url_offer

        return context

@login_required
def edit_lodging_offer_uploads_image(request, slug):
    user = request.user
    profile = user.profile

    # We get the lodging offer
    lodging_offer = LodgingOffer.objects.get(slug=slug)

    # Verifying user owner offer to edit capabilities
    if lodging_offer.created_by != request.user:
        raise Http404

    # Use the LodgingOfferImageForm
    form_class = LodgingOfferImagesForm

    # If we make submit
    if request.method == 'POST':
        # We get data from the submitted form
        form = form_class(data=request.POST, files=request.FILES, instance=lodging_offer)
        if form.is_valid():
            # Create the new LodgingOfferImage object from the submitted form
            LodgingOfferImage.objects.create(
                lodging_offer=lodging_offer, image=form.cleaned_data['image']
            )
            messages.success(request, "La fotografía ha sido cargada y asociada a tu oferta " + lodging_offer.ad_title)
            return redirect('host:edit_lodging_offer_uploads_image', slug=lodging_offer.slug)
    # Otherwise, just create the lodging offer upload image form
    else:
        form = form_class(instance=lodging_offer)

    # We get all images of a LodginOffer object
    uploads = lodging_offer.lodgingofferimage.all()

    # Render to template
    return render(request, 'edit_lodging_offer_images.html', {
        'lodging_offer': lodging_offer,
        'form': form,
        'uploads': uploads,
        'userprofile': profile
    })


class LodgingOfferImageUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = LodgingOfferImage
    form_class = LodgingOfferImagesForm

    # success_url = reverse_lazy("host:edit-study-offer-image", pk_url_kwarg='pk')

    success_message = "Imagen actualizada"

    def get_success_url(self):
        # return reverse("host:edit-study-offer-image", kwargs={self.pk_url_kwarg: self.kwargs.get('pk')})
        return reverse("host:edit-lodging-offer-image",
                       kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(LodgingOfferImageUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        lodging_offer_image = LodgingOfferImage.objects.get(pk=self.kwargs.get('pk'))
        context['lodging_offer_image'] = lodging_offer_image
        return context

    # Permiso para que solo el dueño pueda editarla

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(LodgingOfferImageUpdateView, self).get_object()
        if not obj.lodging_offer.created_by == self.request.user:
            raise Http404
        return obj


@login_required
def delete_lodging_offer_image(request, id):
    # We get the image
    upload = LodgingOfferImage.objects.get(id=id)


    # Security check
    if upload.lodging_offer.created_by != request.user:
        raise Http404

    # Delete image
    upload.delete()
    messages.success(request, 'Tu imágen ha sido borrada, ya no aparecerá en el detalle de tu '
                              'oferta ' + upload.lodging_offer.ad_title)
    # Refresh the edit page
    return redirect('host:edit_lodging_offer_uploads_image', slug=upload.lodging_offer.slug)


@login_required
def delete_upload_study_offer_image(request, id):

    user = request.user
    # We get the image
    upload = StudyOfferImage.objects.get(id=id)


    # Security check
    if upload.study_offer.created_by != request.user:
        raise Http404

    # Delete image
    upload.delete()
    messages.success(request, 'Tu imágen ha sido borrada, ya no aparecerá en el detalle de tu '
                              'oferta ' + upload.study_offer.ad_title)

    # Refresh the edit page
    return redirect('host:edit_study_offer_uploads', slug=upload.study_offer.slug)


def contact_owner_offer(request, lodging_offer_owner_full_name, lodging_offer_owner_email,
                        user_interested_full_name, interested_email, lodging_offer_title,
                        offer_url):
    user = request.user
    if user.is_authenticated:
        # print('Send email')
        mail_subject_to_user = 'Has aplicado a una oferta de alojamiento'
        mail_subject_to_owner = 'Interesados en tu oferta'


        context = {
            # usuario dueño de la oferta  TO
            'lodging_offer_owner_full_name': lodging_offer_owner_full_name,
            #'lodging_offer_owner_enterprise_name': lodging_offer_owner_enterprise_name,
            # 'lodging_offer_owner_username': lodging_offer_owner_username,
            'lodging_offer_owner_email': lodging_offer_owner_email,

            # oferta por la que se pregunta
            'lodging_offer_title': lodging_offer_title,
            'offer_url': offer_url,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            # 'user_interested_username': user_interested_username,
            'interested_email': interested_email,
            'user_interested_full_name': user_interested_full_name,
        }

        msg_to_who_applies = render_to_string('message_to_user_who_applies.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject_to_user, msg_to_who_applies, settings.DEFAULT_FROM_EMAIL,
                  [interested_email], html_message=msg_to_who_applies, fail_silently=True)

        #sleep(60)
        # Hacer esto con celery --- pagina 66 https://docs.google.com/document/d/1aUVRvGFh0MwYZydjXlebaSQJgZnHJDOKx3ccjWmusgc/edit#

        msg_to_owner = render_to_string('to_lodging_own_offer.html', context)
        send_mail(mail_subject_to_owner, msg_to_owner, settings.DEFAULT_FROM_EMAIL,
                  [lodging_offer_owner_email], html_message=msg_to_owner, fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()


class HostingOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = LodgingOffer
    success_url = reverse_lazy("articles:article_list")

    # success_url = reverse_lazy("host:list")
    context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de alojamiento eliminada con éxito"

    def get_success_url(self):
        lodging_offers = self.get_object()
        # print(entrepreneurship_offer)
        # return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
        return reverse_lazy("host:list", kwargs={'username': lodging_offers.created_by.username})

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(HostingOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(HostingOfferDeleteView, self).get_context_data(**kwargs)
        return context


# Add LoginRequiredMixin,
class StudyOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = StudiesOffert
    form_class = StudiesOffertForm
    success_message = "Tu oferta educativa ha sido creada con éxito. " \
                      "A continuación agrega más imágenes para generar " \
                      "mayor interés en los usuarios"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.pub_date = timezone.now()
        form.save()
        return super(StudyOfferCreateView, self).form_valid(form)


class StudyOffertDetailView(LoginRequiredMixin, UserProfileDataMixin, DetailView):
    model=StudiesOffert
    template_name = 'hosts/studyoffert_detail.html'
    context_object_name = 'studyofferdetail'

    def get_context_data(self, **kwargs):
        context = super(StudyOffertDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Ya no, era para tipo de oferta si era de educacion continua o profesional o doctorado
        # studiestype_query = StudiesOffert.objects.get(pk=self.kwargs.get('pk'))
        # studies_type_study_offert = studiestype_query.studies_type_offered.all()
        # context['studiestypeoffered'] = studies_type_study_offert

        # Capturamos quien creo la oferta, y su titulo de anuncio
        study_offer_owner_full_name = self.get_object().created_by.get_long_name()
        print("Nombe completo del dueño", study_offer_owner_full_name)

        # study_offer_owner_username = self.get_object().created_by.username
        # print("Usuario del dueño", study_offer_owner_username)

        study_offer_owner_email = self.get_object().created_by.email
        print('email del dueño ofertassss', study_offer_owner_email)

        study_offer_title = self.get_object().ad_title
        print('titulo oferta', study_offer_title)

        # Capturamos los datos de quien esta interesado en la oferta
        user_interested_email = user.email
        print('email del user interesado oferta', user_interested_email)

        # user_interested_username = user.username
        # print('username del user interesado oferta', user_interested_username)

        user_interested_full_name = user.get_long_name()
        print('Nombre completo del intereadao', user_interested_full_name)

        user_interested_full_name = user.get_long_name()
        print('Nombre completo del intereadao', user_interested_full_name)

        # Capturamos el url de la oferta de estudios
        offer_url = self.request.get_full_path
        print("URL Offer", offer_url)

        study_offer = StudiesOffert.objects.get(slug=self.kwargs.get('slug'))
        # print(study_offer)

        # Obteniendo imágenes
        uploads = study_offer.uploadsstudyoffer.all()


        # Enviamos contextos
        context['uploads'] = uploads
        # context['study_offer_owner_username'] = study_offer_owner_username
        context['study_offer_owner_email'] = study_offer_owner_email
        context['study_offer_owner_full_name'] = study_offer_owner_full_name
        context['study_offer_title'] = study_offer_title

        context['user_interested_email'] = user_interested_email
        # context['user_interested_username'] = user_interested_username
        context['user_interested_full_name'] = user_interested_full_name
        # context['user_interested_enterprise_name'] = user_interested_enterprise_name

        context['offer_url'] = offer_url

        return context


def contact_study_owner_offer(request, study_offer_owner_full_name, study_offer_owner_username,
                                study_offer_owner_email, user_interested_full_name, user_interested_username,
                                user_interested_email,  study_offer_title, offer_url
                              ):
    user = request.user
    print(study_offer_owner_full_name)
    if user.is_authenticated:
        #print('Send email')
        mail_subject_to_user = 'Has aplicado a una oferta educativa'
        mail_subject_to_owner = 'Interesados en tu oferta'

        context = {
            # usuario dueño de la oferta  TO
            'study_offer_owner_full_name': study_offer_owner_full_name,
            'study_offer_owner_username': study_offer_owner_username,
            'study_offer_owner_email': study_offer_owner_email,

            # oferta por la que se pregunta
            'study_offer_title': study_offer_title,
            'offer_url': offer_url,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            'user_interested_username': user_interested_username,
            'user_interested_email': user_interested_email,
            'user_interested_full_name': user_interested_full_name,
            # 'user_interested_enterprise_name': user_interested_enterprise_name,
        }

        msg_to_who_applies = render_to_string('hosts/message_to_user_who_applies.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject_to_user, msg_to_who_applies, settings.DEFAULT_FROM_EMAIL,
                  [user_interested_email], html_message=msg_to_who_applies, fail_silently=True)

        msg_to_owner = render_to_string('hosts/to_educational_own_offer.html', context)

        send_mail(mail_subject_to_owner, msg_to_owner, settings.DEFAULT_FROM_EMAIL,
                  [study_offer_owner_email], html_message=msg_to_owner, fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()



@login_required
def edit_study_offer_uploads(request, slug):

    user = request.user
    profile = user.profile

    # Obtenemos la oferta
    study_offer = StudiesOffert.objects.get(slug=slug)


    # Doublo checking just for security
    # para cuando un usuario que no es quien lo creo intente editarlo
    if study_offer.created_by != request.user:
        raise Http404

    # Seteamos el form que estamos usando
    form_class = StudyOfferImagesUploadForm

    # if we make submit
    if request.method == 'POST':
        # grab the data from the submitted form,
        # note the new "files" part
        form = form_class(data=request.POST, files=request.FILES, instance=study_offer)
        if form.is_valid():
            # create a new object from the submitted form
            StudyOfferImage.objects.create(
                image=form.cleaned_data['image'],
                study_offer=study_offer
            )
            messages.success(request, 'La fotografía ha sido cargada y asociada a la oferta ' + study_offer.ad_title)
            return redirect('host:edit_study_offer_uploads', slug=study_offer.slug)
    # Otherwise just create the form
    else:
        form = form_class(instance=study_offer)

    # grab all the object's images
    uploads = study_offer.uploadsstudyoffer.all()

    # and render the template
    return render(request, 'edit_images_uploads.html', {
        'study_offer': study_offer,
        'form': form,
        'uploads': uploads,
        'userprofile': profile,
    })


class StudyOfferImageUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = StudyOfferImage
    form_class = StudyOfferImagesUploadForm

    # success_url = reverse_lazy("host:edit-study-offer-image", pk_url_kwarg='pk')

    success_message = "Imagen actualizada"

    def get_success_url(self):
        # return reverse("host:edit-study-offer-image", kwargs={self.pk_url_kwarg: self.kwargs.get('pk')})
        return reverse("host:edit-study-offer-image",
                       kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(StudyOfferImageUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        study_offer_image = StudyOfferImage.objects.get(pk=self.kwargs.get('pk'))
        context['study_offer_image'] = study_offer_image
        return context

    # Permiso para que solo el dueño pueda editarla

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(StudyOfferImageUpdateView, self).get_object()
        if not obj.study_offer.created_by == self.request.user:
            raise Http404
        return obj
    '''
    def get_object(self):
        return get_object_or_404(UploadStudyOffer, pk=self.kwargs.get('pk'))
    '''


@login_required
def delete_upload_study_offer_image(request, id):
    # We get the image
    upload = StudyOfferImage.objects.get(id=id)

    # Security check
    if upload.study_offer.created_by != request.user:
        raise Http404

    # Delete image
    upload.delete()
    # Refresh the edit page
    return redirect('host:edit_study_offer_uploads', slug=upload.study_offer.slug)





class StudyOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = StudiesOffert
    form_class = StudiesOffertForm
    # success_url = reverse_lazy("articles:articles_list")
    # success_url = reverse_lazy("hosts:detail-lodging-offer")
    success_message = "Oferta educativa actualizada con éxito"

    def get_context_data(self, **kwargs):
        context = super(StudyOfferUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        return context


    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(StudyOfferUpdateView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


class StudyOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = StudiesOffert
    # success_url = reverse_lazy("articles:article_list")
    # success_url = reverse_lazy("host:list")
    context_object_name = 'studyofferdelete'
    success_message = "Oferta de estudio eliminada con éxito"

    def get_success_url(self):
        educational_offers = self.get_object()
        return reverse_lazy("host:studiesofferlist", kwargs={'username': educational_offers.created_by.username})

    def get_context_data(self, **kwargs):
        context = super(StudyOfferDeleteView, self).get_context_data(**kwargs)
        user = self.request.user
        return context

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(StudyOfferDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj



