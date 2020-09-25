from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve

from account.apps import AccountConfig
from account.models import Position, auto_delete_file_on_delete, auto_delete_file_on_change, Profile
from testfixtures import tempdir, compare
from unittest.mock import Mock
import os


class UserAdvancedFieldCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser', email='test_user@gmail.com', is_active=True)
        self.user.set_password('TU12345678tu')
        self.user.save()
        self.position = Position.objects.create(name='PosName')

    def test_position_base_wrappers(self):
        from . import apps
        a = apps.AccountConfig
        self.assertEqual(a.name, 'account')
        position = Position.objects.get(name='PosName')
        self.assertEqual(str(position), str(self.position))

    @tempdir()
    def test_file_auto_deletion(self, dir):
        dir.write('avatar.png', b'some foo thing')
        instance = Mock()
        instance.avatar.path = os.path.join(dir.path, 'avatar.png')
        auto_delete_file_on_delete(None, instance)
        self.assertFalse(os.path.exists(instance.avatar.path))

    @tempdir()
    def test_file_changing(self, dir):
        dir.write('avatar2.png', b'some foo thing')
        instance = Mock()
        instance.avatar.path = os.path.join(dir.path, 'avatar.png')
        instance.pk = 1

        sender = Mock()
        new_av = Mock()
        new_av.avatar.path = os.path.join(dir.path, 'avatar2.png')

        def get(*args, **kwargs):
            return new_av
        sender.objects.get = get
        auto_delete_file_on_change(sender, instance)
        self.assertFalse(os.path.exists(instance.avatar.path))

        class DoesNotExist(Exception):
            pass
        sender.DoesNotExist = DoesNotExist

        def get(*args, **kwargs):
            raise DoesNotExist()
        sender.objects.get = get
        self.assertFalse(auto_delete_file_on_change(sender, instance))


class AccountViewsCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser', email='test_user@gmail.com', is_active=True)
        self.user.set_password('TU12345678tu')
        self.user.save()
        self.user.profile.bio = 'TestBio'
        self.user.profile.save()
        self.position = Position.objects.create(name='PosName')
        self.c = Client()

    def test_log_in_view(self):
        response = self.c.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.c.get(reverse('account:logout'))
        response = self.c.post(reverse('account:login'), {'email': 'test_user@gmail.com', 'password': 'TU12345678tu'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse('account:login'), {'email': 'test_user@gmail.com', 'password': 'TU12345678tu',
                                                          'next': '/components'})
        self.assertEqual(response.status_code, 302)
        self.c.get(reverse('account:logout'))
        response = self.c.post(reverse('account:login'), {'email': 'test_user@gmail.com', 'password': 'wrong'})
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Login or Password incorrect')

    def test_profile_detail(self):
        self.c.login(username='test_user@gmail.com', password='TU12345678tu')
        response = self.c.get(reverse('account:profile_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].profile.bio, 'TestBio')
        response = self.c.post(reverse('account:profile_detail'), {'first_name': 'First_name',
                                                                   'last_name': 'Last_name'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse('account:profile_detail'), {'first_name': '',
                                                                   'last_name': ''})
        for m in response.context['messages']:
            self.assertEqual(str(m), 'Input incorrect')

        from io import BytesIO
        img = BytesIO(b'mybinarydata')
        img.name = 'myimage.jpg'
        response = self.c.post(reverse('account:profile_upload_avatar'), {'name': 'fred', 'attachment': img})
        self.assertEqual(response.status_code, 405)
        response = self.c.post(reverse('account:profile_upload_avatar'), {'name': 'fred', 'avatar': img})
        self.assertEqual(response.status_code, 200)
        img = BytesIO(bytes(100020))
        response = self.c.post(reverse('account:profile_upload_avatar'), {'name': 'fred', 'avatar': img})
        self.assertEqual(response.status_code, 405)

    def test_team(self):
        self.c.login(username='test_user@gmail.com', password='TU12345678tu')
        response = self.c.get(reverse('account:team'))
        self.assertEqual(len(response.context['team']), 1)

