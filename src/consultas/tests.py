from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profissional

class ProfissionalAPITestCase(APITestCase):

    def setUp(self):
        """
        Roda antes de cada teste, inserindo um profissional com os campos 
        reais do modelo para servir de base no banco temporário.
        """
        self.profissional_teste = Profissional.objects.create(
            nome_social="Dra. Roberta Silva",
            profissao="Cardiologia",
            endereco="Av. Paulista, 1000",
            contato="11999998888"
        )
        self.url_listagem = reverse('profissional-list')

    def test_listar_profissionais(self):
        """Garante que a API consegue listar os profissionais cadastrados"""
        response = self.client.get(self.url_listagem)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome_social'], "Dra. Roberta Silva")

    def test_criar_profissional_valido(self):
        """Garante que a API cadastra um profissional com os campos corretos"""
        dados_novo_profissional = {
            "nome_social": "Dr. Marcos Souza",
            "profissao": "Pediatria",
            "endereco": "Rua das Flores, 123",
            "contato": "11988887777"
        }
        
        response = self.client.post(self.url_listagem, dados_novo_profissional, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 2)
