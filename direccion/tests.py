from django.test import TestCase
from core.models import Direccion


class DirModelTest(TestCase):

    # Crea una dirección correctamente
    def test_create_dir_succesful(self):
        dir_name = 'AgroSuper'
        dir = Direccion.objects.create(
            dir_name = dir_name
        )

        self.assertEqual(dir.dir_name, dir_name)

    # Crear una dirección sin datos
    def test_create_dir_empty_data(self):
        dir = Direccion.objects.create(
            dir_name = ""
        )

        self.assertIsNotNone(dir.dir_name) 