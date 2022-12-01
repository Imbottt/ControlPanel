from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    # Test con email y contraseña correctos
    def test_createa_user_with_email_succesful(self):
        email = 'testUser@email.com'
        password = 'test12345'
        user = get_user_model().objects.create_user(
            email=email, 
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Testea email para nuevo usuario normalizado --> Normalizar= Dejar todo después del @ en minúscula
    def test_new_user_email_normalized(self):
        email = 'testuser@EMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test12345')

        self.assertEqual(user.email, email.lower())

    # PRUEBA EN MANTENIMIENTO
    #def test_new_user_invalid_email(self):
    #    with self.assertRaises(ValueError):
    #        get_user_model().objects.create_user('test12345')