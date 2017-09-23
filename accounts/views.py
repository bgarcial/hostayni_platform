from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from django.views import generic
from django.views.generic.edit import UpdateView

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin

from hostayni.mixins import UserProfileDataMixin



from .forms import (
        StudentProfileForm, ExecutiveProfileForm,
        ProfessorProfileForm, UserCreateForm, UserUpdateForm,
        StudyHostProfileForm, HostingHostProfileForm, )
from .models import (
        StudentProfile, ProfessorProfile,
        ExecutiveProfile, User, UserProfile
        )

User = get_user_model()


@login_required
def user_profile_update_view(request, slug):
    user = request.user

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
            # return redirect('articles:article_list')
            return redirect('home')
    else:
        forms = [x['form'](instance=x['instance']) for x in form_profiles]

    return render(request, 'accounts/profile_form.html', {'forms': forms, 'userprofile':profile,})

class AccountSettingsUpdateView(LoginRequiredMixin, UserProfileDataMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    #success_url = reverse_lazy('articles:article_list')
    success_url = reverse_lazy('home')



class LogoutView(generic.RedirectView):
    # Redirect back to article list
    url = reverse_lazy('articles:article_list')

    # se dispara cuando entra el request entrante
    def get(self, request, *args, **kwargs):
        # Llamamos a logout with the request
        logout(request)
        return super().get(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"