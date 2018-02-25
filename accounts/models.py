from __future__ import unicode_literals

import os
import random
import hashlib

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.contrib import messages

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
    # Model manager of all Django's user model

    PermissionsMixin
    # I have that the users that I create have groups permissions and
    # all benefits of them
)

from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField
# https://github.com/stefanfoulis/django-phonenumber-field

from taggit.managers import TaggableManager
from django.urls import reverse_lazy

from host_information.models import SpeakLanguages, EntertainmentActivities

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.core.mail import EmailMessage


# Model Manager


class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_active', False)
        if not email:
            raise ValueError("Users must have an email address")


        # If the users don't have a user or display name
        # I set as display_name the username they've provided.
        # If some reason signup some user without display_name, this will be
        # the username
        # if not display_name:
        #    display_name = username

        # Make new user, user instance in memory
        user  = self.model(
            # make sure that all the email addresses throughout your app are formatted the same way
            email = self.normalize_email(email),
            **extra_fields

        )
        user.set_password(password)

        # handle the encryption and validation checks and so.
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def get_image_path(instance, filename):
    return os.path.join('userprofile-pictures', str(instance.email), filename)


class User(AbstractBaseUser, PermissionsMixin):

    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, "Masculino"),
        (FEMALE, "Femenino"),
    )

    SPANISH = 'SPA'
    ENGLISH = 'ENG'
    GERMAN = 'DEU'
    FRENCH = 'FRA'
    PORTUGUESE = 'POR'

    LANGUAGES_CHOICES = (
        (SPANISH, 'Español'),
        (ENGLISH, 'Inglés'),
        (GERMAN, 'Alemán'),
        (FRENCH, 'Frances'),
        (PORTUGUESE, 'Portugués'),
    )

    PERSON = 'P'
    ENTERPRISE = 'O'

    USER_TYPE_CHOICES = (
        (PERSON, "Persona"),
        (ENTERPRISE, "Organización"),
    )

    email = models.EmailField(unique=True, null=True, verbose_name='correo electrónico',
            # help_text=_('Required. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.@+-]+$', _('Enter a valid email address.'), 'invalid')
        ])

    username = models.CharField(_('username'), max_length=30, unique=True,
            help_text=_('Required. 30 characters or fewer. Letters, digits and ''@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
        ])

    slug = models.SlugField(
        # unique=True,
        max_length=100,
        blank=True
    )

    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    enterprise_name = models.CharField(_('Nombre de la organización'), max_length=100, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Género',
        # default=False,
        blank=True,
    )

    country_of_origin = CountryField(blank_label='(Seleccione el país)',
                                     verbose_name='Pais de origen',
                                     blank=True,)

    city_of_origin = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Ciudad de origen',

    )
    # Can I use later this package https://github.com/coderholic/django-cities

    country_current_residence = CountryField(
        blank_label='(Seleccione el país)',
        verbose_name = 'País de residencia',
        blank=True,
    )

    city_current_residence = models.CharField(
        max_length=255,
        blank = True,
        verbose_name='Ciudad de residencia'
    )
     # Can I use later this package https://github.com/coderholic/django-cities

    # Adicionarla ahora despues de la migracion

    speak_languages = models.ManyToManyField(
        SpeakLanguages,
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
        verbose_name='Idiomas',
        related_name="users",
        blank=True,
        # here m2m lookup sample
        # https://stackoverflow.com/a/16360605/2773461
    )

    phone_number = PhoneNumberField(
        blank=True,
        help_text="Por favor use el siguiente formato: <em>+Country Code-Number</em>.",
        verbose_name='Número de contacto'
    )

    address = models.CharField(_("Dirección"), max_length=128, blank=True,)

    biography = models.TextField(
        blank=True,
        null=True,
        verbose_name='Biografía',
    )

    description = models.TextField(
        verbose_name='Descripción',
        blank=True,
        null=True,
    )

    avatar = models.ImageField(
        upload_to=get_image_path,
        #upload_to='avatars',
        blank=True,
        null=True,
        verbose_name='Fotografía de perfil',
    )

    date_joined = models.DateTimeField(default=timezone.now)

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    creation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de creación',
        help_text="Por favor use el formato: <em>YYYY-MM-DD</em>.",
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        verbose_name='Tipo de Usuario',
        default=False,
        blank=False,
    )

    '''
    terms_and_conditions = models.BooleanField(
        default=False,
        verbose_name='Aceptar términos y condiciones de uso de HOSTAYNI',
        help_text='Al hacer click en registrarse usted acepta los siguientes',
        blank=False,
        null=False
    )
    '''

    is_student = models.BooleanField(
        default=False,
        verbose_name='Estudiante',

    )

    is_professor = models.BooleanField(
        default=False,
        verbose_name='Profesor',

    )

    is_executive = models.BooleanField(
        default=False,
        verbose_name='Ejecutivo/Emprendedor',
    )

    is_study_host = models.BooleanField(
        default=False,
        verbose_name='Anfitrion de estudio',
    )

    is_innovation_host = models.BooleanField(
        default=False,
        verbose_name='Anfitrión de innovación',

    )

    is_hosting_host = models.BooleanField(
        default=False,
        verbose_name='Anfitrión de alojamiento',

    )

    is_entertainment_host = models.BooleanField(
        default=False,
        verbose_name='Anfitrión de entretenimiento',

    )

    is_other_services_host = models.BooleanField(
        default=False,
        verbose_name='Anfitrión de otros servicios',
    )

    # Adicionarla ahora despues de la migración

    entertainment_activities = models.ManyToManyField(
        EntertainmentActivities,
        blank=True,
        verbose_name='Actividades de entretenimiento',
        help_text='Mantenga presionado "Control" (o "Command" en un Mac), y haga click en las opciones que desea selecionar.',
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    # email is the unique identifier to look people up in the database
    # currently we have the username too, but I want to log in with the
    # email addresses
    USERNAME_FIELD = "email"

    # List of fields that will be sent when create the superuser in addition to
    # username and password
    # REQUIRED_FIELDS = ["username", "email"]
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = 'Usuarios en la plataforma'

    def __str__(self):
        return "@{}".format(self.email)

    def set_avatar(self):
        _avatar = self.avatar
        if not _avatar:
            self.avatar = "img/default_profile_pic.png"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def image_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    def get_short_name(self):
        return self.first_name
        # return self.display_name

    def get_long_name(self):
        return "{} {}".format(self.first_name, self.last_name)
        # return "{} (@{})".format(self.display_name, self.username)

    def get_enterprise_name(self):
        return "{}".format(self.enterprise_name)

    # We get the profiles user according with their type

    def get_student_profile(self):
        student_profile = None
        if hasattr(self, 'studentprofile'):
            student_profile = self.studentprofile
        return student_profile

    def get_professor_profile(self):
        professor_profile = None
        if hasattr(self, 'professorprofile'):
            professor_profile = self.professorprofile
        return professor_profile

    def get_executive_profile(self):
        executive_profile = None
        if hasattr(self, 'executiveprofile'):
            executive_profile = self.executiveprofile
        return executive_profile

    def get_study_host_profile(self):
        study_host_profile = None
        if hasattr(self, 'studyhostprofile'):
            study_host_profile = self.studyhostprofile
        return study_host_profile

    def get_innovation_host_profile(self):
        innovation_host_profile = None
        if hasattr(self, 'innovationhostprofile'):
            innovation_host_profile = self.innovationhostprofile
        return innovation_host_profile

    def get_hosting_host_profile(self):
        hosting_host_profile = None
        if hasattr(self, 'hostinghostprofile'):
            hosting_host_profile = self.hostinghostprofile
        return hosting_host_profile

    def get_entertainment_host_profile(self):
        entertainment_host_profile = None
        if hasattr(self, 'entertainmenthostprofile'):
            entertainment_host_profile = self.entertainmenthostprofile
        return entertainment_host_profile

    def get_other_services_host_profile(self):
        other_services_host_profile = None
        if hasattr(self, 'otherserviceshostprofile'):
            other_services_host_profile = self.otherserviceshostprofile
        return other_services_host_profile

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        #self.avatar =

        # if self.user_type=='O':
        #    FirstName = self.enterprise_name

        if self.is_student and getattr(self, 'studentprofile', None) is None:
            StudentProfile.objects.create(
                user=self,
                slug=self.email
            )
        if self.is_professor and getattr(self, 'professorprofile', None) is None:
            ProfessorProfile.objects.create(
                user=self,
                slug=self.email
            )
        if self.is_executive and getattr(self, 'executiveprofile', None) is None:
            ExecutiveProfile.objects.create(
                user=self,
                slug=self.email
            )
        if self.is_study_host and getattr(self, 'studyhostprofile', None) is None:
            StudyHostProfile.objects.create(
                user=self,
                slug=self.email
            )
        '''
        if self.is_hosting_host and getattr(self, 'hostinghostprofile', None) is None:
            HostingHostProfile.objects.create(
                user=self,
                slug=self.email
            )
        '''


# https://docs.djangoproject.com/en/1.11/ref/signals/#django.db.models.signals.pre_save

# Funcion para no crear un slug similar #ej juan.jaime crea slug juanjaime y juanjaime crea slug juanjaime
# entonces que la cambie
def create_slug(instance, new_slug=None):
    slug = slugify(instance.email)
    if new_slug is not None:
        slug = new_slug
    qs = User.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        # Add the id to slug (compose by email + ID)
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_user_receiver(sender, instance, *args, **kwargs):

    # instance.is_active = False

    if not instance.slug:
        instance.slug = create_slug(instance)
    """
    slug = slugify(instance.email)
    # fabiola.quimica - fabiolaquimica
    # We want to make sure that slug doesn't already exist
    # I will check if exist with a filter
    exists = User.objects.filter(slug=slug).exists()
    if exists:
        # Add the id to slug (compose by email + ID)
        slug = "%s-%s" %(slugify(instance.email), instance.id)

    instance.slug = slug
    """


pre_save.connect(pre_save_user_receiver, sender=settings.AUTH_USER_MODEL)

'''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(sender, instance, **kwargs):
    slug = slugify(instance.email)
    User.objects.filter(pk=instance.pk).update(slug=slug)
'''


class UserProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        # print(dir(self))
        # print(self.instance) # user
        try:
            # Excluyendo mostrar que me sigo a mi mismo
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)  # (user_obj, true)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added = False
        else:
            user_profile.following.add(to_toggle_user)
            added = True
        return added

    # Funcion para saber si estoy siguiendo a alguien
    # recibe el usuario que me sigue
    def is_following(self, user, followed_by_user):
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self, user, limit_to=10):
        print(user)
        profile = user.profile
        # my profile

        following = profile.following.all()
        # profile of the people that I follow

        following = profile.get_following()
        # para evitar recomendarme a mi mismo

        # QUe me excluya de las recomendaciones los usuarios que ya sigo
        qs = self.get_queryset().exclude(user__in=following).exclude(id=profile.id).order_by("?")[:limit_to]
        return qs



# volvera ver Model Manager for following https://www.udemy.com/tweetme-django/learn/v4/t/lecture/6134698?start=0 y el de signals

class UserProfile(models.Model):
    # user.profile
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # user.profile.following -- users I follow
    # user.profile.followed_by -- users that follow me -- reverse relationship
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='followed_by'
    )

    objects = UserProfileManager()  # UserProfile.objects.all()

    # abc = UserProfileManager() # UserProfile.abc.all()

    def __str__(self):
        # return str(self.following.all.count())
        return str(self.user)

    # Para evitar que following a mi mismo mirar follow toggle video
    def get_following(self):
        users = self.following.all()  # Users.objects.all().exclude(email=self.user.email)
        return users.exclude(email=self.user.email)

    def get_follow_url(self):
        return reverse_lazy('accounts:follow', kwargs={"email": self.user.email})


    def get_absolute_url(self):
        return reverse_lazy('accounts:detail', kwargs={"email": self.user.email})

'''
class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,)
    # El hash de activar el usuario
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        # send email here & render a string

        # activation_url = "http://localhost:8000/accounts/activate/%s" %(self.activation_key)
        activation_url = "%s%s" %(settings.SITE_URL, reverse("activation_view", args=[self.activation_key]))
        context = {
            'activation_key': self.activation_key,
            'activation_url': activation_url,
            #'user': self.user.first_name
            'user': self.user.email
        }
        message = render_to_string("accounts/activation_message.txt", context)
        subject = 'Activa tu correo electrónico'
        # print(message)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)

'''




# Signal para que cuando se cree un usuario, se cree su userprofile y se envie un correo de
# confirmación.
# View post_save parametere https://docs.djangoproject.com/en/1.11/ref/signals/#post-save


def user_created(sender, instance, created, *args, **kwargs):
    # user = instance
    #

    if created:
        new_profile = UserProfile.objects.get_or_create(user = instance)
        '''
        # send email to verify user email
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user = instance)
        if email_is_created:
            # create hash
            short_hash = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            # email = user.email
            base, domain = str(instance.email).split("@")
            activation_key = hashlib.sha1(str(short_hash + base).encode('utf-8')).hexdigest()
            # Enviamos el codigo de activacion definido en EmailConfirmed model
            email_confirmed.activation_key = activation_key
            # Lo creamos o guardams
            email_confirmed.save()
            # send email
            email_confirmed.activate_user_email()

            # activation_key = hashlib.sha1(short_hash+email).hexdigest()


            # user.emailedconfirmed.email_user()

            '''

        # print(new_profile, is_created) # print email and true because the user is created
        # celery + redis
        # deferred tasks

    # print('this is the', sender)
    # print('this is the', instance)
    # print('user is', created)


post_save.connect(user_created, sender=settings.AUTH_USER_MODEL)


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    origin_education_school = models.CharField(
        _("Institución de educación de origen"), max_length=128,
        blank=True,
        null=True,
    )

    current_education_school = models.CharField(
        _("Institución educativa en la cual está vinculado en su actual lugar residencia"), max_length=128,
        blank=True,
        null=True,
    )

    extra_occupation = models.CharField(
        _("Ocupación Extra"), max_length=128,
        blank=True,
        null=True,
    )

    educational_titles = models.CharField(
        max_length=255,
        verbose_name='Titulos Educativos',
        blank=True,
        null=True,
    )

    complete_studies_school = models.CharField(
        _("Institución en donde completó sus estudios anteriores"), max_length=255,
        blank=True,
        null=True,
    )

    knowledge_topics_choice = models.CharField(
        _("Áreas de conocimiento de su elección"), max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Usuarios con perfil de estudiantes'

    def __str__(self):
        return "{}".format(self.user.email)


class ProfessorProfile(models.Model):
    CATHEDRAL_PROFESSOR = 'CATHEDRAL'
    RESEARCH_PROFESSOR = 'RESEARCH'
    INSTITUTIONAL_DIRECTIVE = 'DIRECTIVE'

    OCCUPATION_CHOICES = (
        (CATHEDRAL_PROFESSOR, 'Catedrático'),
        (RESEARCH_PROFESSOR, 'Investigador'),
        (INSTITUTIONAL_DIRECTIVE, 'Directivo Institucional'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    occupation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    origin_education_school = models.CharField(
        _("Institución de educación de origen"), max_length=128,
        blank=True,
        null=True,
    )

    current_education_school = models.CharField(
        _("Institución educativa en la cual está vinculado en su actual lugar residencia"),
        max_length=128,
        blank=True,
        null=True,
    )

    educational_titles = models.CharField(
        max_length=255,
        verbose_name='Títulos educativos',
        blank=True,
        null=True,
    )

    complete_studies_school = models.CharField(
        _("Institución en donde terminó sus estudios anteriores"), max_length=255,
        blank=True,
        null=True,
    )

    knowledge_topics_choice = models.CharField(
        _("Areas de conocimiento de su elección"), max_length=255,
        blank=True,
        null=True,
    )

    research_groups = models.CharField(
        _("Grupos de Investigación a los que pertenece"), max_length=255,
        blank=True,

    )


    autorship_publications = models.CharField(
        _("Publications of its authorship"), max_length=255,
        blank=True,

    )


    class Meta:
        verbose_name_plural = 'Usuarios con perfil de profesores'

    def __str__(self):
        return "{}".format(self.user.email, )


class ExecutiveProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    '''
    occupation = models.CharField(
        max_length=255,
        blank = True,
        verbose_name='Occupation',
        # help_text='Hola'
    )
    '''

    enterprise_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Compañía con la cual esta vinculado',
    )

    innovation_topics_choice = models.CharField(
        _("Areas de innovación de su elección"), max_length=255,
        blank=True,
        null=True,
    )

    '''
    companies_to_visit = models.CharField(
        _("Companies to Visit"), max_length=255
    )
    '''

    educational_titles = models.CharField(
        max_length=255,
        verbose_name='Títulos educativos',
        blank=True,
        null=True,
    )

    complete_studies_school = models.CharField(
        _("Institución en donde terminó sus estudios anteriores"), max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Usuarios con perfil de ejecutivos'

    def __str__(self):
        return "{}".format(self.user.email, )


class StudyHostProfile(models.Model):
    UNIVERSITY = 'Universidad'
    UNIVERSITY_INSTITUTION = 'Institución Universitaria'
    PROFESSIONAL_TECH_INSTITUTION = 'Institución Tecnológica Profesiona'
    CEC = 'Centro de Educación Contínua'

    INSTITUTION_TYPE_CHOICES = (
        (UNIVERSITY, 'Universidad'),
        (UNIVERSITY_INSTITUTION, 'Institución Universitaria'),
        (PROFESSIONAL_TECH_INSTITUTION, 'Institución Técnica y/o Tecnológica '),
        (CEC, 'Centro de Educación Contínua'),
        (CEC, 'Centro de Educación para la vida y el trabajo'),
    )

    PRIVATE = 'PRIVATE'
    PUBLIC = 'PUBLIC'
    MIXED = 'MIXED'

    CHARACTER_INSTITUTE_CHOICES = (
        (PRIVATE, "Privada"),
        (PUBLIC, "Pública"),
        (MIXED, "Privada - Pública"),
    )

    NATIONAL_ACCREDITATIONS = 'Acreditación Nacional'
    INTERNATIONAL_ACCREDITATIONS = 'Acreditación Internacional'

    ACCREDITATIONS_CHOICES = (
        (NATIONAL_ACCREDITATIONS, "Acreditación Nacional"),
        (INTERNATIONAL_ACCREDITATIONS, "Acreditación Internacional"),
    )

    LESS_THAN_THOUSAND = 'Menos de 1.000 estudiantes'
    ONE_THOUSAND_TEN_THOUSAND = 'Entre 1.000 y 10.000 estudiantes'
    TEN_THOUSAND_TWENTY_THOUSAND = 'Entre 10.000 y 20.000 estudiantes'
    GREATER_THAN_TWENTY_THOUSAND = 'Mayor a 20.000 estudiantes'

    STUDENT_NUMBERS_CHOICES = (
        (LESS_THAN_THOUSAND, 'Menos de 1.000 estudiantes'),
        (ONE_THOUSAND_TEN_THOUSAND, 'Entre 1.000 y 10.000 estudiantes'),
        (TEN_THOUSAND_TWENTY_THOUSAND, 'Entre 10.000 y 20.000 estudiantes'),
        (GREATER_THAN_TWENTY_THOUSAND, 'Mayor a 20.000 estudiantes'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    institution_type = models.CharField(
        max_length=255,
        choices=INSTITUTION_TYPE_CHOICES,
        verbose_name='Tipo de institución',
    )

    institute_character = models.CharField(
        max_length=7,
        choices=CHARACTER_INSTITUTE_CHOICES,
        verbose_name='Caracter de la institución',
    )

    high_quality_accreditations = models.CharField(
        _("Acreditaciones de alta calidad"), max_length=255
    )

    students_number = models.CharField(
        max_length=255,
        choices=STUDENT_NUMBERS_CHOICES,
        verbose_name='Número de estudiantes'
    )

    rankings_classification = models.TextField(
        _("Clasificación en ranking")
    )

    knowledge_topics = TaggableManager(
        verbose_name="Áreas de conocimiento",
        # help_text= tag_helptext()
        help_text=_("Una lista de temas separada por comas.")
    )


    class Meta:
        verbose_name_plural = 'Usuarios con perfil de anfitriones de estudio'

    def __str__(self):
        return "{}".format(self.user.email, )


class InnovationHostProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Usuarios con perfil de anfitriones de innovación'

    def __str__(self):
        return "{}".format(self.user.display_name, )

'''
class HostingHostProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )


    additional_description = models.TextField(
        null=False,
        blank=False
    )


    class Meta:
        verbose_name_plural = 'Usuarios con perfil de anfitriones de hospedaje'

    def __str__(self):
        return "{}".format(self.user.email, )

'''


class EntertainmentHostProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Usuarios con perfil de anfitriones de entretenimiento'

    def __str__(self):
        return "{}".format(self.user.display_name, )


class OtherServicesHostProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'Usuarios con perfil de anfitriones de servicios varios'

    def __str__(self):
        return "{}".format(self.user.display_name, )
