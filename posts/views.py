from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from hostayni.mixins import UserProfileDataMixin
from django.views.generic import(
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect

from .forms import PostModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from accounts.models import User, UserProfile

class RepostView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if request.user.is_authenticated():
            # Llamamos al PostManager y le pasamos el user que hace el repost y el post
            new_post = Post.objects.repost(request.user, post)
            # Retornamos el nuevo post (reposteado) con su url haciendo uso de get_absolute_url
            return HttpResponseRedirect("/post")
        # sino, retornamos el post original con su url
        return HttpResponseRedirect(post.get_absolute_url())


# Create
# https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-editing/#createview

class PostCreateView(UserProfileDataMixin, FormUserNeededMixin, CreateView):
    form_class = PostModelForm
    template_name = 'posts/create_view.html'
    # success_url = reverse_lazy('post:detail')
    # login_url = '/accounts/login/'
    # fields = ['user', 'content']

    '''
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            return super(PostCreateView, self).form_valid(form)
        else:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue"])
            return self.form_invalid(form)
    '''


'''
def post_create_view(request):
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.user = request.user
        instance.save()
    context = {
        "form": form
    }
    return render(request, 'posts/create_view.html', context)
'''


class PostUpdateView(LoginRequiredMixin, UserProfileDataMixin, UserOwnerMixin, UpdateView):
    queryset = Post.objects.all()
    form_class = PostModelForm
    template_name = 'posts/update_view.html'
    success_url = '/post/'


class PostDeleteView(LoginRequiredMixin, UserProfileDataMixin, DeleteView):
    # queryset = Post.objects.all()
    model = Post
    template_name = 'posts/delete_confirm.html'
    success_url = reverse_lazy('post:list')


# List Posts


class PostListView(LoginRequiredMixin, UserProfileDataMixin, ListView):
    # template_name = "posts/post_list2.html"
    # queryset = Post.objects.all().order_by('-updated')
    # queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = Post.objects.all().order_by('-updated')
        # print(self.request.GET)
        query = self.request.GET.get("q", None)
        if query is not None:
            # qs = qs.filter(content__icontains=query)
            # Mirar esto
            # https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, *kwargs)
        user = self.request.user

        following = UserProfile.objects.is_following(self.request.user, self.object_list)
        context['following'] = following

        # Pasamos el form de crear post para que aparezca en el post list
        context['create_form'] = PostModelForm()

        # Pasamos el url que me permite hacer un POST de un post
        context['create_url'] = reverse_lazy("post:create")

        if user.is_authenticated():
            context['userprofile'] = user.profile
        return context

'''
def post_list_view(request):
    queryset = Post.objects.all()
    print(queryset)
    for obj in queryset:
        print(obj.content)
    context = {
        "object_list": queryset
    }
    return render(request, "posts/list_view.html", context)
'''


class PostDetailView(UserProfileDataMixin,DetailView):
    # template_name = "posts/detail_view.html" go to post_detail.html template
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        # Pasando context userprofile para borrar o actualizar post desde
        # el detalle de post, hacerlo en el post list del layout en JS
        context['userprofile'] = user.profile
        return context

    def get_object(self):
        # print(self.kwargs)
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        return obj

'''
def post_detail_view(request, pk=None): # pk=id
    # obj = Post.objects.get(pk=pk)
    obj = get_object_or_404(Post, pk=pk)
    # print(obj)
    context = {
        "object": obj
    }

    return render(request, "posts/detail_view.html", context)
'''