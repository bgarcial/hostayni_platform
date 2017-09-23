from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail

from blog.models import Article, Comment
from blog.forms import ArticleForm, CommentForm, EmailPostForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from hostayni.mixins import UserProfileDataMixin
from django.contrib.auth.decorators import login_required


from django.views.generic import (ListView, DetailView,
                                    CreateView, UpdateView,
                                    DeleteView)
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.


def article_share(request, slug):
    # Retrieve article by id
    article = get_object_or_404(Article, slug=slug,
        published_date__lte=timezone.now())

    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(
                                          article.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], article.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(article.title, article_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'hostayni@gmail.com', [cd['to']])
            sent = True
            print(sent)
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html',
                 {'article': article,
                 'form': form,
                 'sent': sent})



def articles_by_user(request, email):
    user = request.user
    profile = user.profile
    articles = Article.objects.filter(author__email=user.email)
    return render(
        request,
        'blog/my_articles.html',
        {'articles': articles,
        'userprofile': profile})


class ArticleListView(UserProfileDataMixin, ListView):
    template_name = 'hostayni/home.html'
    model = Article
    paginate_by = 2

    # Permite usar el django ORM en las CBV genericas solamente
    # para personalizar el query acorde a lo que queremos es como un
    # sql query sobre mi modelo
    # Ver documentacion de field lookups
    # https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups
    def get_queryset(self):
        return Article.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class ArticleDetailView(UserProfileDataMixin, DetailView):
    model = Article


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


class CreateArticleView(LoginRequiredMixin, UserProfileDataMixin, CreateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog/article_detail.html'
    form_class = ArticleForm

    model=Article

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user
        form.save()
        return super(CreateArticleView, self).form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserProfileDataMixin, UpdateView):
    login_url = 'accounts/login/'
    redirect_field_name = 'blog/article_detail.html'
    form_class = ArticleForm

    model=Article


class ArticleDeleteView(LoginRequiredMixin, UserProfileDataMixin, DeleteView):
    model=Article
    success_url = reverse_lazy('articles:article_list')


class ArticleDraftListView(LoginRequiredMixin, UserProfileDataMixin, ListView):
    login_url = '/login/'
    # redirect_field_name = 'blog/article_list.html'
    template_name = 'ihost/home2.html'

    model = Article

    def get_queryset(self):
        return Article.objects.filter(published_date__isnull=True).order_by('created_date')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def article_publish(request, slug):
    article = get_object_or_404(Article, slug=slug)
    # View publish method in Article model
    article.publish()
    return redirect('articles:article_detail', slug=slug)

@login_required
def add_comment_to_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # Queremos conectar ese comentario particular de un articulo
            # a un objeto articulo y grabarlo
            # ver en modelo Comment la F.K article
            comment.article = article
            comment.save()
            return redirect('article_detail', pk=article.pk)
    # Pero si el request method no es un POST, es decir, que alguien
    # no ha llenado el formulario de comentario, pinte el formulario
    # y pasamos en el contexto, un diccionario que contiene el form
    # a renderizar
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # View approve method in Comment model which set one Comment object
    # to approved_comment = True
    comment.approve()
    return redirect('article_detail', pk=comment.article.pk)
    # Un comment esta conectado a un articulo particular en el modelo
    # Comment


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    article_pk = comment.article.pk
    comment.delete()
    return redirect('article_detail', pk=article_pk)
















