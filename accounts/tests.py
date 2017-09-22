from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import UserProfile

# Create your tests here.

User = get_user_model()


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.email = "andres@gmail.com"
        new_user = User.objects.create(email=self.email)

    def test_profile_created(self):
        email = self.email
        user_profile = UserProfile.objects.filter(user__email=self.email)
        print(user_profile)
        self.assertTrue(user_profile.exists())
        self.assertTrue(user_profile.count() == 1)

    # Por si se crea un usuario repetido
    def test_new_user(self):
        new_user = User.objects.create(email=self.email + "abcsd")