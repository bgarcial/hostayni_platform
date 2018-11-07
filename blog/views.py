from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.core.mail import send_mail

from carousel_offers.models import HomeCarousel

from blog.models import Article, Category
from blog.forms import ArticleForm
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from hostayni.mixins import UserProfileDataMixin
from django.contrib.auth.decorators import login_required


from django.views.generic import (ListView, DetailView,
                                    CreateView, UpdateView,
                                    DeleteView)
from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.db.models import Count
from taggit.models import Tag

# Create your views here.


# ****--- fbv CRUD blog posts ---*****

def categories(request, id):

    categories = Category.objects.all()
    cat = Category.objects.get(pk=id)
    articles = Article.objects.filter(category=cat)
    context = {
        'categories': categories,
        'cat': cat,
        'articles': articles,
    }
    return render(request, 'hostayni/home.html', context)

@login_required
def article_create(request):
    user = request.user
    #if not user.is_staff or not user.is_superuser:
    #    raise Http404
    #if not user.is_authenticated:
    #    raise Http404

    # Tomamos el request dentro del formulario
    # Para poder crear un articulo, adjuntar su imagen es necesario request.FILES or NOne
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.publish = timezone.now()
        # print(form.cleaned_data.get('title'))
        # print(form.cleaned_data.get('content'))
        instance.save()
        # message success
        messages.success(request, "Tus artículo ha sido creado con éxito")
        return HttpResponseRedirect(instance.get_absolute_url())

    # Rendering form errors in a view
    if form.has_error:
        # print(form.errors.as_json())
        # print(form.errors.as_text())
        data = form.errors.items()
        for key, value in data:
        #    print(dir(value))
            error_str = "{field}: {error}".format(
                field=key,
                error=value.as_text()
            )
            # print(error_str)
        # print(form.non_field_errors)
        # Falta que se limpien los campos delmformulario
        #title = form.cleaned_data.get('title')
        #form.cleaned_data.get('title')
        #form.cleaned_data.get('title')

    context = {
        'form': form,
    }
    if user.is_authenticated():
        context['userprofile'] = user.profile
    return render(request, 'article_form.html', context)


def artic_detail(request, slug=None, tag_slug=None): # retrieve
    user = request.user
    # instance = Article.objects.get(id=3)
    # instance = get_object_or_404(Article, title='Hola, esto es una pruea')

    # Como no lo hemos cambiado a .all() sino que seguims con el get_object_404
    # cambiamos en el manager de all a active para que funcione el detail
    instance = get_object_or_404(Article, slug=slug)

    object_list = Article.objects.all()

    # Si un usuario anonimo entra al detalle de un articulo que esta en draft
    # no lo encontrara
    # if instance.draft or instance.publish > timezone.now().date():
    if instance.publish > timezone.now().date() or instance.draft:
        if not user.is_active:
            raise Http404

    tag = None
    if tag_slug:
        # we build the initial QuerySet, retrieving
        # all active publications, and if there is a given
        # tag slug, we get the Tag object with the given slug
        # using the get_object_or_404() shortcut.
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # List of similar posts
    post_tags_ids = instance.tags.values_list('id', flat=True)
    similar_posts = Article.objects.filter(tags__in=post_tags_ids) \
        .exclude(id=instance.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]


    context = {
        'title': instance.title,
        'instance': instance,
        'similar_posts':similar_posts,
        'tag':tag
    }
    if user.is_authenticated():
        context['userprofile'] = user.profile

    return render(request, 'article_detail.html', context)


class ArticleListView(UserProfileDataMixin, ListView):
    template_name = 'hostayni/home.html'
    model = Article
    # paginate_by = 4
    # context_object_name = article_list


    # Permite usar el django ORM en las CBV genericas solamente
    # para personalizar el query acorde a lo que queremos es como un
    # sql query sobre mi modelo
    # Ver documentacion de field lookups
    # https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups
    def get_queryset(self):
        queryset_list = Article.objects.active()

        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset_list = Article.objects.all()

        query = self.request.GET.get("q")
        if query is not None:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                # Q(category__title__icontains=query) |
                Q(author__full_name__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        return queryset_list
        #return Article.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        #categories = Category.objects.all()
        #cat = Category.objects.get(pk=)
        #context['categories'] = categories
        sliders = HomeCarousel.objects.all_featured()
        today = timezone.now().date()
        context['today'] = today
        context['sliders'] = sliders
        return context


# It takes an optional tag_slug parameter that has
# a None default value. This parameter will come in the URL.
def article_list(request, tag_slug=None):
    user = request.user

    sliders = HomeCarousel.objects.all_featured()

    # Capturamos la fecha actual
    today = timezone.now().date()

    # queryset_list = Article.objects.filter(draft=False).filter(publish__lte=timezone.now()) #all() #.order_by('-timestamp')
    queryset_list = Article.objects.active() #.order_by('-timestamp')



    # Que me liste tambien los articulos draft o con fecha de publicacion mayor a la actual si es un super usuario
    # o user.is_staff
    # if user.is_staff or user.is_superuser:
    #    queryset_list = Article.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(author__full_name__icontains=query)
                ).distinct()

    '''
    paginator = Paginator(queryset_list, 4)  # Show 5 articles per page

    page_request_var = "page"

    page = request.GET.get(page_request_var) # parametro en el url ?page=x
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    '''
    object_list = Article.objects.all()
    tag = None
    if tag_slug:
        # we build the initial QuerySet, retrieving
        # all active publications, and if there is a given
        # tag slug, we get the Tag object with the given slug
        # using the get_object_or_404() shortcut.
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = queryset_list.filter(tags__in=[tag])

    context = {
        'article_list':queryset_list,
        #'title': "List is working",
        #'page_request_var': page_request_var,
        'sliders':sliders,
        'today': today,
        'tag': tag
    }
    if user.is_authenticated():
        context['userprofile'] = user.profile
    return render(request, 'hostayni/home.html', context)


@login_required
def article_update(request, slug=None):
    user = request.user
    #if not user.is_staff or not user.is_superuser:
    #    raise Http404
    instance = get_object_or_404(Article, slug=slug)
    if instance.author != user:
        raise Http404
    # Para poder actualizar un articulo, su imagen es necesario request.FILES or NOne
    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # form.instance.author = request.user
        instance.save()
        # message success
        # messages.success(request, "<a href='#'>Item</a>Saved", extra_tags='html_safe')
        messages.success(request, "Tu artículo ha sido actualizado")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    if user.is_authenticated():
        context['userprofile'] = user.profile
    return render(request, 'blog/article_form.html', context)


def article_delete(request, slug=None):
    user = request.user
    #if not user.is_staff or not user.is_superuser:
    #    raise Http404
    instance = get_object_or_404(Article, slug=slug)
    instance.delete()
    messages.success(request, "Tu artículo ha sido borrado")
    return redirect("articles:article_list")


def articles_by_user(request, username):
    user = request.user
    profile = user.profile
    articles = Article.objects.filter(author__username=user.username)
    return render(
        request,
        'blog/my_articles.html',
        {'articles': articles,
        'userprofile': profile})


class ArticleDetailView(UserProfileDataMixin, DetailView):
    model = Article

'''
def article_detail(request, slug):
    user = request.user
    article = get_object_or_404(Article, slug=slug)
    # Add a QuerySet to retrieve all active comments for this post:
    comments = article.comments.filter(active=True)
    context = {'article': article, 'comments': comments}
    # context = {'article': article}
    if user.is_authenticated():
        context['userprofile'] = user.profile

        if request.method == 'POST':
            # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # cd = comment_form.cleaned_data
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current article to the comment we just created
                # By doing this, we are specifying that the new comment belongs to the given post.
                new_comment.article = article
                # Save the comment to the database
                new_comment.save()
        else:
            comment_form = CommentForm()
        context['comment_form'] = comment_form
    return render(request, 'blog/article_detail.html',
                  context)
'''


class CreateArticleView(LoginRequiredMixin, UserProfileDataMixin, CreateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog/article_detail.html'
    form_class = ArticleForm

    model = Article

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.instance.publish = timezone.now()
        print(timezone.now())
        form.save()
        messages.success(self.request, "Tu artículo ha sido exitosamente creado")
        return super(CreateArticleView, self).form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserProfileDataMixin, UpdateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog/article_detail.html'
    form_class = ArticleForm

    model=Article
    # messages.success(self.request, "Successfully created")

    # Permiso para que solo el dueño pueda editarla
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ArticleUpdateView, self).get_object()
        # print (obj.author)
        if not obj.author == self.request.user:
            raise Http404
        return obj


class ArticleDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserProfileDataMixin, DeleteView):
    model=Article
    # success_url = reverse_lazy('articles:article_list')
    success_message = "Tu artículo ha sido eliminado exitosamente"

    def get_success_url(self):
        articles = self.get_object()
        # print(entrepreneurship_offer)
        # return reverse_lazy("offer:list", kwargs={'created_by': entrepreneurship_offer.created_by.username})
        return reverse_lazy("articles:list", kwargs={'username': articles.author.username})

    '''
    def get_context_data(self, **kwargs):
        context = super(ArticleDeleteView, self).get_context_data(**kwargs)
        user = self.request.user
        article = Article.objects.get(slug=self.kwargs.get('slug')) # borrando articulo
        context['article'] = article
        return context
    '''

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ArticleDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj


class ArticleDraftListView(LoginRequiredMixin, UserProfileDataMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'blog/article_list.html'
    template_name = 'ihost/home2.html'

    model = Article

    def get_queryset(self):
        return Article.objects.filter(published_date__isnull=True).order_by('created_date')


