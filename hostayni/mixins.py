# from django.contrib.auth import get_user_model
from accounts.models import User
# from accounts.forms import UserUpdateForm


class UserProfileDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserProfileDataMixin, self).get_context_data(**kwargs)
        user = self.request.user
        #context['userprofile'] = user.profile
        if user.is_authenticated():
            context['userprofile'] = user.profile
        return context


class ProfileImageUser(object):
    def get_context_data(self, **kwargs):
        context = super(ProfileImageUser, self).get_context_data(**kwargs)
        user = User.objects.filter(username=self.request.user.username)
        # model = get_user_model()
        # form_class = UserUpdateForm
        return context