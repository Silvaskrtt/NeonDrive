from django.test import TestCase
from apps.clients.models import Client

class ClientTest(TestCase):

    def test_create_client(self):

        client = Client.objects.create(
            name="Teste",
            cpf="12345678900",
            email="teste@email.com",
            phone="99999-0000"
        )

        self.assertEqual(client.name, "Teste")