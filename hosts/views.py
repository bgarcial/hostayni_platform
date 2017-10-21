from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.forms import modelformset_factory
from django.http import HttpResponseNotModified, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic import DeleteView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User
from hostayni.mixins import UserProfileDataMixin
from rest_framework import viewsets

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from .models import LodgingOffer, StudiesOffert, RoomInformation, LodgingOfferImage

from host_information.models import OfferedServices, FeaturesAmenities
from .serializers import LodgingOfferSerializer,StudiesOffertSerializer

from .forms import (LodgingOfferForm, StudiesOffertForm, LodgingOfferSearchForm,
                    StudiesOffertSearchForm, LodgingOfferImagesForm)

from django.views.generic.edit import FormView
from haystack.query import SearchQuerySet
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail

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

def studies_offers_by_user(request, email):
    user = request.user
    profile = user.profile
    studies_offers = StudiesOffert.objects.filter(created_by__email=user.email)

    return render(
        request,
        'hosts/studiesoffer_list.html',
        {'studies_offers':studies_offers,
        'userprofile':profile}
    )

'''
class LodgingOffersByUser(LoginRequiredMixin, ListView):
    template_name = 'hosts/lodgingoffer_list2.html'

    def get_context_data(self, **kwargs):
        context = super(LodgingOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        lodging_offers = LodgingOffer.objects.filter(created_by__username=self.request.user)
        context['offers_by_user'] = lodging_offers

        if user.is_authenticated():
            context['userprofile'] = user.profile
        return context
'''

def lodging_offers_by_user(request, email):
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
class LodgingOfferImageCreate(UserProfileDataMixin, CreateView):
    model = LodgingOffer
    fields = ['ad_title', 'country', 'city', 'address', 'lodging_offer_type', 'stars',
              'check_in', 'check_out', 'offered_services', 'featured_amenities',
              'room_type_offered', 'number_guest_room_type', 'bed_type', 'bathroom',
              'room_information', 'image', 'room_value', 'additional_description', 'is_taked']
    # success_url = reverse_lazy("articles:article_list")

    def get_context_data(self, **kwargs):
        data = super(LodgingOfferImageCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lodgingimages'] = LodgingOfferImagesFormset(self.request.POST)
        else:
            data['lodgingimages'] = LodgingOfferImagesFormset()
            return data

    def form_valid(self, form):
        context = self.get_context_data()
        lodgingimages = context['lodgingimages']
        print('contexto enviado', lodgingimages)
        with transaction.atomic():
            self.object = form.save()

            if lodgingimages.is_valid():
                lodgingimages.instance = self.object
                lodgingimages.save()
        return super(LodgingOfferImageCreate, self).form_valid(form)

'''


class HostingOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = LodgingOffer
    form_class = LodgingOfferForm
    #success_url = reverse_lazy("articles:article_list")
    success_message = "Oferta de alojamiento creada con éxito"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.save()
        # success_message = "Oferta de estudio creada con éxito"
        return super(HostingOfferCreateView, self).form_valid(form)

    '''
    
    def post(self, request, *args, **kwargs):
        print('post arrive')
        ImageFormSet = modelformset_factory(LodgingOfferImage, form=LodgingOfferImagesForm, extra=3)
        lodging_offerForm = LodgingOfferForm(self.request.POST)
        formset = ImageFormSet(self.request.POST, self.request.FILES,
                               queryset=LodgingOfferImage.objects.none())

        print('Request del usuario antes de validar el form', self.request.user)

        if lodging_offerForm.is_valid() and formset.is_valid():
            lodging_offer_form = lodging_offerForm.save(commit=False)
            print('Request del usuario despues de validado el form', request.user.id)
            lodging_offer_form.created_by_id = self.request.user.id
            lodging_offer_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = LodgingOfferImage(lodging_offer=lodging_offer_form, image=image)
                photo.save()
            messages.success(self.request,
                             "Yeeew,check it out on the home page!")
            #return redirect('host:detail', slug=self.slug_url_kwarg)
            #return HttpResponseRedirect(lodging_offer_form.get_absolute_url())
            #return self.form_valid(form)
        return super(HostingOfferCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print('Request del usuario', self.request.user)
        context = super(HostingOfferCreateView, self).get_context_data(**kwargs)
        ImageFormSet = modelformset_factory(LodgingOfferImage,
                                            form=LodgingOfferImagesForm, extra=3)
        lodging_offerForm = LodgingOfferForm()
        formset = ImageFormSet(queryset=LodgingOfferImage.objects.none())
        context['lodging_offerForm'] = lodging_offerForm
        context['formset'] = formset
        return context

    '''







class HostingOfferUpdateView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, UpdateView):
    model = LodgingOffer
    form_class = LodgingOfferForm
    #success_url = reverse_lazy("dashboard")
    # success_url = reverse_lazy("hosts:detail-lodging-offer")
    success_message = "Oferta de alojamiento actualizada con éxito"

    def get_context_data(self, **kwargs):
        context = super(HostingOfferUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        return context


class HostingOfferDetailView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model = LodgingOffer
    template_name = 'lodgingoffer_detail.html'
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
        lodging_offer_owner_enterprise_name = self.get_object().created_by.get_enterprise_name
        lodging_offer_owner_email = self.get_object().created_by.email
        lodging_offer_title = self.get_object().ad_title

        # Capturamos los datos de quien esta interesado en la oferta
        user_interested_email = user.email
        user_interested_full_name = user.get_long_name()


        url_offer = self.request.get_full_path
        # print(url_offer)

        context['lodging_offer_owner_email'] = lodging_offer_owner_email
        context['lodging_offer_owner_full_name'] = lodging_offer_owner_full_name
        context['lodging_offer_owner_enterprise_name'] = lodging_offer_owner_enterprise_name
        context['lodging_offer_title'] = lodging_offer_title

        context['user_interested_email'] = user_interested_email
        context['user_interested_full_name'] = user_interested_full_name

        context['offer_url'] = url_offer

        #contact_owner_offer(self.request, lodging_offer_owner_email, user_interested_email, lodging_offer_title)

        return context


def contact_owner_offer(request, lodging_offer_owner_full_name, lodging_offer_owner_email,
                        user_interested_full_name, interested_email, lodging_offer_title, offer_url):
    user = request.user
    if user.is_authenticated:
        # print('Send email')
        mail_subject = 'Interesados en tu oferta'


        context = {
            # usuario dueño de la oferta  TO
            'lodging_offer_owner_full_name': lodging_offer_owner_full_name,
            #'lodging_offer_owner_enterprise_name': lodging_offer_owner_enterprise_name,
            'lodging_offer_owner_email': lodging_offer_owner_email,

            # oferta por la que se pregunta
            'lodging_offer_title': lodging_offer_title,
            'offer_url': offer_url,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            'interested_email': interested_email,
            'user_interested_full_name': user_interested_full_name,
        }

        message = render_to_string('contact_user_own_offer.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL,
                  [lodging_offer_owner_email, interested_email], fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()


class HostingOfferDeleteView(SuccessMessageMixin, UserProfileDataMixin, LoginRequiredMixin, DeleteView):
    model = LodgingOffer
    success_url = reverse_lazy("articles:article_list")
    # success_url = reverse_lazy("host:list")
    context_object_name = 'lodgingofferdelete'
    success_message = "Oferta de alojamientio eliminada con éxito"

    def get_context_data(self, **kwargs):
        context = super(HostingOfferDeleteView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_student:
            profile = user.get_student_profile()
            context['userprofile'] = profile
        elif user.is_professor:
            profile = user.get_professor_profile()
            context['userprofile'] = profile
        elif user.is_executive:
            profile = user.get_executive_profile()
            context['userprofile'] = profile
        elif user.is_study_host:
            profile = user.get_study_host_profile()
            context['userprofile'] = profile
        elif user.is_hosting_host:
            profile = user.get_hosting_host_profile()
            context['userprofile'] = profile
        elif user.is_active:
            #profile = user.get_user_profile()
            context['userprofile'] = self.request.user
        return context


# Add LoginRequiredMixin,
class StudyOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = StudiesOffert
    form_class = StudiesOffertForm
    #success_url = reverse_lazy("host:detail")
    #success_url = reverse_lazy("dashboard")
    success_message = "Oferta de estudio creada con éxito"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.instance.pub_date = timezone.now()
        form.save()
        return super(StudyOfferCreateView, self).form_valid(form)



class StudyOffertDetailView(LoginRequiredMixin, UserProfileDataMixin, DetailView):
    model=StudiesOffert
    template_name = 'studyoffert_detail.html'
    context_object_name = 'studyofferdetail'

    def get_context_data(self, **kwargs):
        context = super(StudyOffertDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        # Ya no, era para tipo de oferta si era de educacion continua o profesional o doctorado
        # studiestype_query = StudiesOffert.objects.get(pk=self.kwargs.get('pk'))
        # studies_type_study_offert = studiestype_query.studies_type_offered.all()
        # context['studiestypeoffered'] = studies_type_study_offert

        # Capturamos quien creo la oferta, y su titulo de anuncio
        study_offer_owner_full_name = self.get_object().created_by.get_enterprise_name()
        study_offer_owner_email = self.get_object().created_by.email

        print('email del dueño oferta', study_offer_owner_email)

        study_offer_title = self.get_object().ad_title
        print('titulo oferta', study_offer_title)

        # Capturamos los datos de quien esta interesado en la oferta
        user_interested_email = user.email
        print('email del user interesado oferta', user_interested_email)
        user_interested_full_name = user.get_long_name()

        # Capturamos el url de la oferta de estudios
        url_offer = self.request.get_full_path

        # Enviamos contextos
        context['study_offer_owner_email'] = study_offer_owner_email
        context['study_offer_owner_full_name'] = study_offer_owner_full_name
        context['study_offer_title'] = study_offer_title

        context['user_interested_email'] = user_interested_email
        context['user_interested_full_name'] = user_interested_full_name

        context['url_offer'] = url_offer

        return context


def contact_study_owner_offer(request, study_offer_owner_full_name, study_offer_owner_email,
                              user_interested_full_name, user_interested_email, study_offer_title, url_offer):
    user = request.user
    if user.is_authenticated:
        #print('Send email')
        mail_subject = 'Interesados en tu oferta educativa'



        context = {
            # usuario dueño de la oferta  TO
            'study_offer_owner_full_name': study_offer_owner_full_name,
            'study_offer_owner_email': study_offer_owner_email,

            # oferta por la que se pregunta
            'study_offer_title': study_offer_title,
            'url_offer': url_offer,
            'domain': settings.SITE_URL,
            'request': request.get_full_path,

            # usuario interesado en la oferta
            'user_interested_email': user_interested_email,
            'user_interested_full_name': user_interested_full_name,
        }

        message = render_to_string('contact_study_own_offer.html', context)
        #to_email = lodging_offer_owner.email,

        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL,
                  [study_offer_owner_email, user_interested_email], fail_silently=True)

        #messages.success(request, "El anfitrión", lodging_offer_owner_email, "ha sido contactado " )

    #return redirect('host:contact_owner_offer', lodging_offer_owner_email=lodging_offer_owner_email,
                    #interested_email=interested_email, slug=slug)
    return HttpResponseNotModified()



class StudyOfferUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = StudiesOffert
    form_class = StudiesOffertForm
    # success_url = reverse_lazy("articles:articles_list")
    # success_url = reverse_lazy("hosts:detail-lodging-offer")
    success_message = "Oferta de estudio actualizada con éxito"


    def get_context_data(self, **kwargs):
        context = super(StudyOfferUpdateView, self).get_context_data(**kwargs)

        user = self.request.user
        return context


class StudyOfferDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = StudiesOffert
    success_url = reverse_lazy("articles:article_list")
    # success_url = reverse_lazy("host:list")
    context_object_name = 'studyofferdelete'
    success_message = "Oferta de estudio eliminada con éxito"

    def get_context_data(self, **kwargs):
        context = super(StudyOfferDeleteView, self).get_context_data(**kwargs)

        user = self.request.user
        if user.is_student:
            profile = user.get_student_profile()
            context['userprofile'] = profile
        elif user.is_professor:
            profile = user.get_professor_profile()
            context['userprofile'] = profile
        elif user.is_executive:
            profile = user.get_executive_profile()
            context['userprofile'] = profile
        elif user.is_study_host:
            profile = user.get_study_host_profile()
            context['userprofile'] = profile
        elif user.is_hosting_host:
            profile = user.get_hosting_host_profile()
            context['userprofile'] = profile
        elif user.is_active:
            #profile = user.get_user_profile()
            context['userprofile'] = self.request.user
        return context




'''
class ContactOwnOfferView(View):

    # Debe recibir el request de quien contacta, el pk de la oferta por la cual contacta y el
    # email de la persona a contactar
    def get(self, request, email, pk, *args, **kwargs):
        #Capturamos el email del usuario al que queremos contactar (dueño de la oferta)
        user_to_contact = get_object_or_404(User, email__iexact=email)

        # Debemos capturar la oferta por la cual contacta
        offer_to_interest = get_object_or_404(LodgingOffer, pk=pk)

        # Si el usuario quien presiona contactar al dueño de la ofera esta autenticado
        if request.user.is_authenticated():
            is_contacting = UserProfile.objects.toggle_contact_own_offer(request.user, user_to_contact, offer_to_interest)
        return redirect('hosts:detail', pk=pk)
'''