from django.contrib.auth.models import User
from django.test import TestCase

from account.models import Position, auto_delete_file_on_delete, auto_delete_file_on_change
from testfixtures import tempdir, compare
from unittest.mock import  Mock
import os


class UserAdvancedFieldCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Testuser', email='test_user@gmail.com', is_active=True)
        self.user.set_password('TU12345678tu')
        self.user.save()
        self.position = Position.objects.create(name='PosName')

    def get(*args, **kwargs):
        pass

    def test_position_base_wrappers(self):
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



