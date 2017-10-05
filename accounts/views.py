from __future__ import unicode_literals

import re

from django.contrib.auth import get_user_model

from django.views import generic
from django.views.generic.edit import UpdateView

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from hostayni.mixins import UserProfileDataMixin
from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

from .forms import (
        StudentProfileForm, ExecutiveProfileForm,
        ProfessorProfileForm, UserCreateForm, UserUpdateForm,
        StudyHostProfileForm, HostingHostProfileForm, )

from .models import (
        StudentProfile, ProfessorProfile,
        ExecutiveProfile, User, UserProfile, EmailConfirmed
        )

User = get_user_model()


@login_required
def user_profile_update_view(request, slug):
    user = request.user

    # llamando al mensaje en donde estara el link de activación
    #Necesito llamar esta funcion en el login
    # user.emailconfirmed.activate_user_email()

    # Populate the forms and Instances (if applicable)
    form_profiles = []
    profile = user.profile

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

    if user.is_hosting_host:
        profile = user.get_hosting_host_profile()
        form_profiles.append({'form': HostingHostProfileForm, 'instance': user.hostinghostprofile, 'title': "Hosting Host Details"})

    if request.method == 'POST':
        forms = [x['form'](data=request.POST, instance=x['instance'],) for x in form_profiles]
        if all([form.is_valid() for form in forms]):
            for form in forms:
                form.save()
            return redirect('articles:article_list')
            #return redirect('home')
    else:
        forms = [x['form'](instance=x['instance']) for x in form_profiles]

    return render(request, 'accounts/profile_form.html', {'forms': forms, 'userprofile':profile,})


class AccountSettingsUpdateView(LoginRequiredMixin, UserProfileDataMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    #success_url = reverse_lazy('articles:article_list')
    success_url = reverse_lazy('articles:article_list')



class LogoutView(generic.RedirectView):
    # Redirect back to article list
    url = reverse_lazy('articles:article_list')
    success_message = "Has cerrado sesión, vuelve pronto!"

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

def activation_view(request, activation_key):
    # print(SHA1_RE.search(activation_key))
    if SHA1_RE.search(activation_key):
        print('activation key is real')

        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "Hubo algún error con tu solicitud.")
            return HttpResponseRedirect('/')
            #return HttpResponseRedirect('%s'%(reverse('articles:article_list')))

        if instance is not None and not instance.confirmed:
            print('El correo electrónico ha sido confirmado')
            page_message = 'El correo electrónico ha sido confirmado, Bienvenido'
            instance.confirmed = True
            # Set activation_key to confirmed word, because don't need key in this moment
            instance.activation_key = 'Confirmed'
            instance.save()
            messages.success(request,"Has confirmado tu correo de forma exitosa, Por favor inicia sesión")

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