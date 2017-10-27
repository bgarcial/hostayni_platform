from __future__ import unicode_literals

import re

from django.contrib.auth import get_user_model

from django.views import generic
from django.views.generic.edit import UpdateView
from django.views import View

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from hostayni.mixins import UserProfileDataMixin
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.signals import user_logged_in

from .forms import (
        StudentProfileForm, ExecutiveProfileForm,
        ProfessorProfileForm, UserCreateForm, UserUpdateForm,
        StudyHostProfileForm, )

from .models import (
        StudentProfile, ProfessorProfile,
        ExecutiveProfile, User, UserProfile, EmailConfirmed
        )

from hosts.models import LodgingOffer

# --- Packages to signup and activate fbv's ---
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.http import HttpResponse
# --- End Packages to signup and activate fbv's ---

User = get_user_model()


def show_login_message(sender, user, request, **kwargs):
    # whatever...
    messages.info(request, 'Bienvenido a HOSTAYNI.')


user_logged_in.connect(show_login_message)


@login_required
def user_profile_update_view(request, slug):
    user = request.user

    # llamando al mensaje en donde estara el link de activación
    #Necesito llamar esta funcion en el login
    # user.emailconfirmed.activate_user_email()

    # Populate the forms and Instances (if applicable)
    form_profiles = []
    profile = user.profile
    print(profile)

    if user.is_student:
        profile = user.get_student_profile()
        form_profiles.append({'form': StudentProfileForm,
                              'instance': user.studentprofile,
                              'title':"Student Details"
                            })
    if user.is_professor:
        profile = user.get_professor_profile()
        form_profiles.append({'form': ProfessorProfileForm, 'instance': user.professorprofile, 'title': "Professor Details"})

    if user.is_executive:
        profile = user.get_executive_profile()
        form_profiles.append({'form': ExecutiveProfileForm, 'instance': user.executiveprofile, 'title': "Executive Details"})

    if user.is_study_host:
        profile = user.get_study_host_profile()
        form_profiles.append({'form': StudyHostProfileForm, 'instance': user.studyhostprofile, 'title': "Study Host Details"})

    #if user.is_hosting_host:
        # profile = user.get_hosting_host_profile()
        # form_profiles.append({'form': HostingHostProfileForm, 'instance': user.hostinghostprofile, 'title': "Hosting Host Details"})

    if request.method == 'POST':
        forms = [x['form'](data=request.POST, instance=x['instance'],) for x in form_profiles]
        if all([form.is_valid() for form in forms]):
            for form in forms:
                form.save()
            messages.success(request, "Tus datos de roles de usuario han sido actualizados")
            return redirect('articles:article_list')
            #return redirect('home')
    else:
        forms = [x['form'](instance=x['instance']) for x in form_profiles]

    return render(request, 'accounts/profile_form.html', {'forms': forms, 'userprofile':profile,})


class AccountSettingsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    success_message = "Perfil actualizado exitosamente"
    success_url = reverse_lazy('articles:article_list')
    # success_url = reverse_lazy('accounts:preferences', kwargs={'slug': user.slug})

    # Mirar como redireccionar a esta misma vista despues del post


def logout_view(request):
    logout(request)
    messages.success(request, "<strong>Has cerrado sesión</strong>, <a href='%s'>vuelve pronto!</a>" %(reverse('login')), extra_tags='safe, abc')
    # messages.warning(request, "Existe un warning!")
    # messages.error(request, "Existe un error!")
    return HttpResponseRedirect('%s'%(reverse('articles:article_list')))


class LogoutView(SuccessMessageMixin, generic.RedirectView):
    # Redirect back to article list
    success_message = "Has cerrado sesión, vuelve pronto!"
    url = reverse_lazy('articles:article_list')
    #template_name = "hostayni/home.html"


    # se dispara cuando entra el request entrante
    def get(self, request, *args, **kwargs):
        # Llamamos a logout with the request
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(SuccessMessageMixin, generic.CreateView):
    # llamando al mensaje en donde estara el link de activación
    form_class = UserCreateForm
    success_message = "Registro exitoso, por favor confirma tu correo electrónico ahora antes de iniciar sesión"
    #success_url = reverse_lazy("login")
    success_url = reverse_lazy("articles:article_list")
    template_name = "accounts/signup.html"


SHA1_RE = re.compile('^[a-f0-9]{40}$')

from django.contrib.auth import authenticate

def activation_view(request, activation_key):
    # print(SHA1_RE.search(activation_key))
    if SHA1_RE.search(activation_key):
        print('activation key is real')
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
            # user_= instance.user
            # user_.is_active = True
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "Hubo algún error con tu solicitud.")
            return HttpResponseRedirect('/')
            #return HttpResponseRedirect('%s'%(reverse('articles:article_list')))

        if instance is not None and not instance.confirmed:

            # instance.is_active = True
            #user = User.objects.get(pk=pk)
            #print(user)
            #user.is_active = True

            print('El correo electrónico ha sido confirmado')
            page_message = 'El correo electrónico ha sido confirmado, Bienvenido'
            instance.confirmed = True
            # Set activation_key to confirmed word, because don't need key in this moment
            instance.activation_key = 'Confirmed'
            instance.save()

            messages.success(request,"Has confirmado tu correo de forma exitosa, <a href='%s'>Por favor inicia sesión</a>" %(reverse('login')), extra_tags='safe, abc')

        elif instance is not None and instance.confirmed:
            print('Ya confirmaste tu dirección de correo electrónico')
            page_message = 'Ya confirmaste tu dirección de correo electrónico'
            messages.success(request, "Ya confirmaste tu dirección de correo electrónico")

        else:
            page_message = ''

        context = {'page_message':page_message}
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                #'domain': current_site.domain,
                'domain': settings.SITE_URL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'HOSTAYNI - Activa tu cuenta'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, "Registro exitoso. Te hemos enviado un enlace para que confirmes tu correo electrónico. Por favor hazlo para poder iniciar sesión")
            #return HttpResponse('Please confirm your email address to complete the registration')
            return redirect('login')
    else:
        form = UserCreateForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        messages.success(request,
                         "Has confirmado tu correo de forma exitosa. Ya puedes iniciar sesión")
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.success(request,
                         "Tu correo electrónico ya ha sido confirmado con HOSTAYNI")
        #return HttpResponse('Activation link is invalid!')
        return redirect('login')


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

