from django.test import TestCase

from api.models import User
from api.views import RegisterView, ServicesStatus


class TestGenerateToken(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            login="test",
            surname="test",
            name="test",
            email="test@test.test",
            company="test"
        )

    def test_generate_token_for_user(self):
        user = User.objects.get(login="test")
        self.assertEqual(RegisterView.generate_token(user)[1], 'success')


class TestConvertBase64(TestCase):
    file = None
    file_path = 'qwe.txt'

    def setUp(self) -> None:
        with open('qwe.txt', 'w') as f:
            f.write('asddsdfjkffdsf')

        self.file = open('qwe.txt', 'rb')

    def test_convert_base64(self):
        self.assertEqual(
            ServicesStatus.convert2base64(self.file, self.file_path),
            'success'
        )

