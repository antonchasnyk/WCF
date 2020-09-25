from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from WCF.backends import EmailBackend
from WCF.context_processors.side_menu import side_menu


class UserAuthenticateCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser', email='test_user@gmail.com', is_active=True)
        self.user.set_password('TU12345678tu')
        self.user.save()

        self.user2 = User(username='Testuser2', email='test_user@gmail.com', is_active=True)
        self.user2.set_password('TU12345678tu2')
        self.user2.save()

        self.in_active_user = User.objects.create(username='Inactive', email='Inactive@gmail.com',
                                                  password='Inactive12345678', is_active=False)
        self.in_active_user.set_password('Inactive12345678')
        self.in_active_user.save()

        self.superuser = User.objects.create(username='superuser', email='superuser@gmail.com',
                                             is_active=True, is_staff=True)
        self.superuser.set_password('Superuser12345678')
        self.superuser.save()

    def test_item_base_wrapper(self):
        user = User.objects.get(username='Testuser')
        self.assertEqual(self.user, user)

        user = authenticate(username='test_user@gmail.com', password='TU12345678tu')
        self.assertEqual(self.user, user)

        user_wrong_password = authenticate(username='test_user@gmail.com', password='TU12345678tu223')
        self.assertEqual(None, user_wrong_password)

        user2 = User.objects.get(username='Testuser2')
        self.assertEqual(self.user2, user2)

        user2 = authenticate(username='test_user@gmail.com', password='TU12345678tu2')
        user2_wrong_password = authenticate(username='test_user@gmail.com', password='TU12345678tu212313')
        self.assertEqual(None, user2)
        self.assertEqual(None, user2_wrong_password)

        in_active_user = authenticate(username='Inactive@gmail.com', password='Inactive12345678')
        self.assertEqual(in_active_user, None)

        superuser = authenticate(username='superuser@gmail.com', password='Superuser12345678')
        self.assertEqual(self.superuser, superuser)

        does_not_exist = authenticate(username='supaaaeruser@gmail.com', password='Superuser12345678')
        self.assertEqual(does_not_exist, None)


class SideMenuContextCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_menu_link(self):
        request = self.factory.get(reverse('items:dashboard'))
        new_context = side_menu(request)
        self.assertEqual(new_context['dash'], 'active')

        request = self.factory.get(reverse('purchase:needs'))
        new_context = side_menu(request)
        self.assertEqual(new_context['purch'], 'active')
        self.assertEqual(new_context['purch_needs'], 'active')
