from django import template
from django.contrib.auth import get_user_model
from ..models import UserProfile

register = template.Library()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
User = get_user_model()
@register.inclusion_tag("accounts/snippets/recommend.html")
def recommended(user):
    if isinstance(user, User):
        qs = UserProfile.objects.recommended(user)
        return {"recommended": qs}