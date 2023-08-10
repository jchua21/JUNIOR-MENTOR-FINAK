from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile

class CreateUserTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.image.url, "/media/profiles/default.jpg")
        self.assertEqual(profile.cursos.count(), 0)
        self.assertEqual(profile.user.username, 'testuser')

