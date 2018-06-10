# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.db.models import Q

# from django.views.generic.base import TemplateView
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from .mixins import UserProfileDataMixin
from .forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib import messages
from django.core.urlresolvers import reverse

User = get_user_model()



def contact(request):
    user = request.user

    form_class = ContactForm
    context = {}
    if user.is_authenticated():
        context['userprofile'] = user.profile
        # print(user.profile)
        if request.method == 'POST':
            form = form_class(data=request.POST)
            if form.is_valid():
                contact_name = form.cleaned_data['contact_name']
                contact_email = form.cleaned_data['contact_email']
                form_content = form.cleaned_data['form_content']

                template = get_template('contact_template.txt')

                context = {
                    'contact_name': contact_name,
                    'contact_email': contact_email,
                    'form_content': form_content,
                }

                # return render(request, 'contact.html', {'form': form_class}, context )

                content = template.render(context)
                mail_subject = 'Hola Hostayni, ' + contact_name + ' - ' + contact_email + ' desea contactar contigo'
                email = EmailMessage(
                    mail_subject,
                    content,
                    contact_email,
                    ['info@hostayni.com'],
                    headers={'Reply-To': contact_email}
                )
                email.send()
                messages.success(request,
                                 ' ' + contact_name + '. Tu mensaje ha sido enviado al equipo de Hostayni, te responderemos lo mas pronto posible <a href="%s">Ir al Inicio</a>' % reverse(
                                     'articles:article_list'), extra_tags='safe, abc')

                return redirect('contact')
        return render(request, 'contact.html', {'form': form_class, 'userprofile':user.profile})

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            form_content = form.cleaned_data['form_content']

            template = get_template('contact_template.txt')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }

            content = template.render(context)
            mail_subject = 'Hola Hostayni, ' + contact_name + ' - ' + contact_email + ' desea contactar contigo'
            email = EmailMessage(
                mail_subject,
                content,
                contact_email,
                ['info@hostayni.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            messages.success(request,
            ' ' + contact_name + '. Tu mensaje ha sido enviado al equipo de Hostayni, te responderemos lo mas pronto posible <a href="%s">Ir al Inicio</a>' %reverse('articles:article_list'), extra_tags='safe, abc')

            return redirect('contact')
        #if user.is_authenticated():

    return render(request, 'contact.html', {'form': form_class},)


class HomePageView(UserProfileDataMixin, TemplateView):
    template_name = 'hostayni/home-bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        user = self.request.user
        #context['userprofile'] = user.profile
        if user.is_authenticated():
            context['userprofile'] = user.profile
        # else:
        return context


class WhoWeArePageView(UserProfileDataMixin, TemplateView):
    template_name = 'who_we_are.html'

class HowItWorksPageView(UserProfileDataMixin, TemplateView):
    template_name = 'how_it_works.html'

class HowItWorks2PageView(UserProfileDataMixin, TemplateView):
    template_name = 'how_it_works2.html'



class TermsAndConditions(UserProfileDataMixin, TemplateView):
    template_name = 'terms_and_conditions.html'


class PrivacyPolicy(UserProfileDataMixin, TemplateView):
    template_name = 'privacy-policy.html'


# Buscando Users en hostayni social

class SearchView(UserProfileDataMixin, ListView):
    template_name = 'search.html'
    model = get_user_model()

    def get_context_data(self, **kwargs):
        query = self.request.GET.get("q")
        qs = None
        if query:
            qs = User.objects.filter(
                Q(username__icontains=query) |
                Q(full_name__icontains=query)
                # Aca podriamos buscar por cualquier atributo
                # relacionado con el usuario o del usuario
                # # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
                # http://www.michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/ gran referencia
            )
        context = super(SearchView, self).get_context_data(**kwargs)
        context["users"] = qs
        return context

    '''
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        qs = None
        if query:
            qs = User.objects.filter(
                Q(username__icontains=query) |
                Q(full_name__icontains=query)
                # Aca podriamos buscar por cualquier atributo
                # relacionado con el usuario o del usuario
                # # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
            )
        context = {"users": qs}

        return render(request, "search.html", context)
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        qs = User.objects
        if query:
            qs = qs.filter(
                Q(username__icontains=query) |
                Q(full_name__icontains=query)
            )
        return qs

    '''








def home(request):
    context = {}
    return render(request, 'hostayni/home.html', context)



def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")