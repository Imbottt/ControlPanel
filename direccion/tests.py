from django.test import TestCase
from core.models import Direccion


class DirModelTest(TestCase):

    def setUp(self):
        Direccion.objects.create(dir_name='AgroSuper')
        Direccion.objects.create(dir_name='Process S.A.')

    def test_existe_dir(self):
        exists = Direccion.objects.filter(dir_name='AgroSuper').exists()
        self.assertEqual(exists, True)

    def test_no_existe_dir(self):
        not_exists = Direccion.objects.filter(dir_name='Paradise').exists()
        self.assertEqual(not_exists, False)

    def test_empty_dir(self):
        empty_dir = Direccion.objects.create(dir_name='')
        self.assertIsNotNone(empty_dir, True)