from __future__ import unicode_literals
from django.views.generic.edit import (CreateView, UpdateView,)
from django.views.generic import DeleteView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from hostayni.mixins import UserProfileDataMixin
from rest_framework import viewsets

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from .models import LodgingOffer, StudiesOffert, RoomInformation

from host_information.models import OfferedServices, FeaturesAmenities
from .serializers import LodgingOfferSerializer,StudiesOffertSerializer

from .forms import (LodgingOfferForm,
    StudiesOffertForm, LodgingOfferSearchForm, StudiesOffertSearchForm)

from django.views.generic.edit import FormView
from haystack.query import SearchQuerySet
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

        '''
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
        '''
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
        '''
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
        '''
        return context

def studies_offers_by_user(request, email):
    user = request.user
    profile = user.profile
    studies_offers = StudiesOffert.objects.filter(created_by__email=user.email)

    if user.is_study_host:
        profile = user.get_study_host_profile()


    return render(
        request,
        'hosts/studiesoffer_list.html',
        {'studies_offers':studies_offers,
        'userprofile':profile}
    )


class LodgingOffersByUser(LoginRequiredMixin, ListView):
    template_name = 'hosts/lodgingoffer_list2.html'

    def get_context_data(self, **kwargs):
        context = super(LodgingOffersByUser, self).get_context_data(**kwargs)
        user = self.request.user
        lodging_offers = LodgingOffer.objects.filter(created_by__username=self.request.user)
        context['offers_by_user'] = lodging_offers

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


def lodging_offers_by_user(request, email):
    user = request.user
    profile = user.profile
    lodging_offers = LodgingOffer.objects.filter(created_by__email=user.email)

    if user.is_hosting_host:
        profile = user.get_hosting_host_profile()


    return render(
        request,
        'hosts/lodgingoffer_list.html',
        {'lodging_offers':lodging_offers,
        'userprofile':profile}
    )


# Add LoginRequiredMixin,
class HostingOfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, CreateView):
    model = LodgingOffer
    form_class = LodgingOfferForm
    #success_url = reverse_lazy('dashboard')
    success_message = "Oferta de alojamiento creada con éxito"

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.created_by = self.request.user
        form.save()
        # success_message = "Oferta de estudio creada con éxito"
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



class HostingOfferDetailView(UserProfileDataMixin, LoginRequiredMixin, DetailView):
    model=LodgingOffer
    template_name = 'lodgingoffer_detail.html'
    context_object_name = 'lodgingofferdetail'

    def get_context_data(self, **kwargs):
        context = super(HostingOfferDetailView, self).get_context_data(**kwargs)
        user = self.request.user

        roominformation = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))
        room_information_lodging_offer = roominformation.room_information.all()
        #inf = self.kwargs['room_information_set.all()']

        #room_information = set(queryset.values_list('room_information__name', flat=True).distinct())

        context['lodgingoffer'] = room_information_lodging_offer

        #queryset2 = LodgingOffer.objects.filter(offered_services__lodgingserviceoffer=LodgingServiceOffer.objects.all())

        #offeredservices = set(queryset2.values_list('offered_services__name', flat=True).distinct())

        offeredservices = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))

        query = offeredservices.offered_services.all()

        context['offeredservices'] = query

        featuredamenities = LodgingOffer.objects.get(pk=self.kwargs.get('pk'))

        fe_amen_query = featuredamenities.featured_amenities.all()
        context['featuredamenities'] = fe_amen_query

        return context


class HostingOfferDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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



class StudyOffertDetailView(LoginRequiredMixin, DetailView):
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


        #scholarships_query = StudiesOffert.objects.get(pk=self.kwargs.get('pk'))
        #scholarships = scholarships_query.scholarships.all()
        #context['scholarships'] = scholarships


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


class StudyOfferUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = StudiesOffert
    form_class = StudiesOffertForm
    # success_url = reverse_lazy("articles:articles_list")
    # success_url = reverse_lazy("hosts:detail-lodging-offer")
    success_message = "Oferta de estudio actualizada con éxito"


    def get_context_data(self, **kwargs):
        context = super(StudyOfferUpdateView, self).get_context_data(**kwargs)

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