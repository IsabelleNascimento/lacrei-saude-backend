from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profissional

class ProfissionalAPITestCase(APITestCase):

    def setUp(self):
        """
        Criar dados iniciais no banco de dados de teste isolado.
        """
        self.profissional_teste = Profissional.objects.create(
            nome="Dra. Roberta Silva",
            especialidade="Cardiologia",
            crm="123456/SP",
            telefone="11999998888",
            email="roberta.silva@email.com",
            ativo=True
        )
        # Caminho da URL de listagem de profissionais
        self.url_listagem = reverse('profissional-list')

    def test_listar_profissionais(self):
        """Garante que a API consegue listar os profissionais cadastrados"""
        response = self.client.get(self.url_listagem)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Dra. Roberta Silva")

    def test_criar_profissional_valido(self):
        """Garante que a API consegue cadastrar um novo profissional com dados válidos"""
        dados_novo_profissional = {
            "nome": "Dr. Marcos Souza",
            "especialidade": "Pediatria",
            "crm": "654321/SP",
            "telefone": "11988887777",
            "email": "marcos.souza@email.com",
            "ativo": True
        }
        
        response = self.client.post(self.url_listagem, dados_novo_profissional, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 2)
