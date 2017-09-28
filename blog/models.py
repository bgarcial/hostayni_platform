from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save

from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone


# Model manager es una forma de controlar como
# los modelos trabajan
# Article.objects.all()
# Article.objects.create(user=user, title='Some title')
class ArticleManager(models.Manager):
    # Override the default .all() method
    # # Article.objects.all() = super(ArticleManager, self).all()
    def active(self, *args, **kwargs):
        return super(ArticleManager, self).filter(draft=False).filter(publish__lte=timezone.now())

# Controlando como son subidas las im[agenes con
# el id del post se crea una carpeta y se guarda con su nombre de earhcivo
# puede ser instance.user o cualquier atributo que sea, usarlo apra los nombre sde archivos y fotografias
def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    # return "%s/%s/%s.%s" % ('article_images', instance.id, instance.id, extension)
    # article_images/id_article/id_article.extension

    #return "%s/%s/%s/" %('article_images', instance.id, filename)
    # article_images/id_article.extension

    return "%s/%s" % (instance.id, filename)


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=100, blank=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)

    # Digital Marketplace cubre como manipular y oredenar imagenes en thumbnails
    image = models.ImageField(upload_to= upload_location, null=False, blank=False,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    # Cada vez que se grabe en la base de datos se actualice el campo updated
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Este campo sera grabado solo una vez cuando se cree el articulo
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = ArticleManager()

    '''
    image = models.ImageField(
        upload_to='article_images',
        blank=True,
        null=True,
        verbose_name='Image'
        # width_field="width_field",
        # height_field="height_field"
        # https://www.youtube.com/watch?v=Bmvd1O5pNIY&list=PLEsfXFp6DpzQFqfCur9CJ4QnKQTVXUsRy&index=29
    )
    # width_field=models.IntegerField(default=0)
    # height_field=models.IntegerField(default=0)
    '''
    # updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True,null=True)

    # Asi puedo grabar una imagen por defecto
    #def publish(self):
    #    self.published_date = timezone.now()
    #    self.save()


    # def approve_comments(self):
    #    return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        # return "/articles/%s/" %(self.slug)
        return reverse("articles:detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-timestamp", "-updated"]
        # Otra forma de garantizar un orden ascendente o al mas reciente
        # si no tengo timestamp es hacerlo por pk reverse o reverse id
        # ordering = ['-id', "-timestamp", "-updated"]
        # Lo otro es que si tengo una fecha de publicacion genial


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



def pre_save_article_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_article_receiver, sender=Article)

class Comment(models.Model):
    article = models.ForeignKey('blog.Article', related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()

    # We use the created field to sort comments in chronological order by default.
    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    # active boolean field that we will use to manually deactivate
    # inappropriate comments.
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('updated',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.article)

