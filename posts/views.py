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
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView

from .forms import PostModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin

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

# List Posts


class PostListView(LoginRequiredMixin, UserProfileDataMixin, ListView):
    # template_name = "posts/post_list2.html"
    # queryset = Post.objects.all().order_by('-updated')

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
                Q(user__email__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(PostListView, self).get_context_data(*args, *kwargs)
        # print(context)
        # context["another_list"] = Post.objects.all()
        # print(context)

        # Pasamos el form de crear post para que aparezca en el post list
        context['create_form'] = PostModelForm()

        # Pasamos el url que me permite hacer un POST de un post
        context['create_url'] = reverse_lazy("post:create")
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
    template_name = "posts/detail_view.html"
    queryset = Post.objects.all()

    def get_object(self):
        #print(self.kwargs)
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Post, pk=pk)
        return obj

def post_detail_view(request, pk=None): # pk=id
    # obj = Post.objects.get(pk=pk)
    obj = get_object_or_404(Post, pk=pk)
    # print(obj)
    context = {
        "object": obj
    }

    return render(request, "posts/detail_view.html", context)