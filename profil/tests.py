from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileTests(TestCase):

    def setUp(self):
        # Membuat pengguna untuk pengujian
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            jenis_makanan_favorit='Pizza',
            preferensi_makanan='Vegetarian'
        )

    def test_user_profile_creation(self):
        """Test untuk memastikan profil pengguna dibuat dengan benar."""
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.jenis_makanan_favorit, 'Pizza')
        self.assertEqual(self.user_profile.preferensi_makanan, 'Vegetarian')

    def test_user_profile_update(self):
        """Test untuk memastikan profil pengguna dapat diperbarui."""
        self.user_profile.jenis_makanan_favorit = 'Sushi'
        self.user_profile.save()
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.jenis_makanan_favorit, 'Sushi')

    def test_user_profile_list_view(self):
        """Test untuk memastikan view profil pengguna dapat diakses."""
        self.client.login(username='testuser', password='testpassword')  # Login pengguna
        response = self.client.get(reverse('profil:user_profile_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile_list.html')

    def test_user_profile_detail_view(self):
        """Test untuk memastikan view detail profil pengguna dapat diakses."""
        self.client.login(username='testuser', password='testpassword')  # Login pengguna
        response = self.client.get(reverse('profil:user_profile_detail', args=[self.user_profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile_detail.html')

    def test_user_profile_update_view(self):
        """Test untuk memastikan view pembaruan profil pengguna dapat diakses."""
        self.client.login(username='testuser', password='testpassword')  # Login pengguna
        response = self.client.get(reverse('profil:user_profile_update', args=[self.user_profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile_update.html')

    def test_login_required_for_user_profile_update(self):
        """Test untuk memastikan login diperlukan untuk mengakses pembaruan profil pengguna."""
        self.client.logout()  # Pastikan pengguna logout
        response = self.client.get(reverse('profil:user_profile_update', args=[self.user_profile.id]))
        self.assertRedirects(response, f'/login?next=/profil/user-profile/{self.user_profile.id}/update/')
