from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profissional, Consulta


class ProfissionalAPITestCase(APITestCase):

    def setUp(self):
        """
        Roda antes de cada teste, autenticando o client e inserindo um
        profissional base no banco temporário de testes.
        """
        self.user = User.objects.create_user(username='testuser', password='senha123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.profissional_teste = Profissional.objects.create(
            nome_social="Dra. Roberta Silva",
            profissao="Cardiologia",
            endereco="Av. Paulista, 1000",
            contato="11999998888"
        )
        self.url_listagem = reverse('profissional-list')
        self.url_detalhe = reverse('profissional-detail', args=[self.profissional_teste.id])

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

    def test_criar_profissional_dado_ausente_deve_falhar(self):
        """Garante que a API rejeita a criação sem um campo obrigatório (profissao)"""
        dados_incompletos = {
            "nome_social": "Dr. Sem Profissão",
            "endereco": "Rua Teste, 1",
            "contato": "11900000000"
        }

        response = self.client.post(self.url_listagem, dados_incompletos, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('profissao', response.data)

    def test_atualizar_profissional(self):
        """Garante que a API atualiza corretamente os dados de um profissional existente"""
        dados_atualizados = {
            "nome_social": "Dra. Roberta Silva",
            "profissao": "Cardiologia Pediátrica",
            "endereco": "Av. Paulista, 2000",
            "contato": "11999998888"
        }

        response = self.client.put(self.url_detalhe, dados_atualizados, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profissional_teste.refresh_from_db()
        self.assertEqual(self.profissional_teste.profissao, "Cardiologia Pediátrica")
        self.assertEqual(self.profissional_teste.endereco, "Av. Paulista, 2000")

    def test_excluir_profissional(self):
        """Garante que a API remove um profissional existente"""
        response = self.client.delete(self.url_detalhe)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profissional.objects.count(), 0)

    def test_acesso_sem_token_deve_falhar(self):
        """Garante que a API bloqueia acesso sem autenticação"""
        self.client.credentials()  # remove o token
        response = self.client.get(self.url_listagem)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ConsultaAPITestCase(APITestCase):

    def setUp(self):
        """
        Roda antes de cada teste, autenticando o client e inserindo um
        profissional e uma consulta base no banco temporário de testes.
        """
        self.user = User.objects.create_user(username='testuser2', password='senha123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.profissional = Profissional.objects.create(
            nome_social="Dr. João Pereira",
            profissao="Psiquiatria",
            endereco="Rua Augusta, 500",
            contato="11977776666"
        )
        self.outro_profissional = Profissional.objects.create(
            nome_social="Dra. Ana Costa",
            profissao="Dermatologia",
            endereco="Rua Oscar Freire, 300",
            contato="11966665555"
        )
        self.consulta_teste = Consulta.objects.create(
            data="2026-08-10T14:30:00Z",
            profissional=self.profissional
        )
        self.url_listagem = reverse('consulta-list')
        self.url_detalhe = reverse('consulta-detail', args=[self.consulta_teste.id])

    def test_listar_consultas(self):
        """Garante que a API consegue listar as consultas cadastradas"""
        response = self.client.get(self.url_listagem)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_criar_consulta_valida(self):
        """Garante que a API cadastra uma consulta vinculada a um profissional"""
        dados_nova_consulta = {
            "data": "2026-09-01T10:00:00Z",
            "profissional": self.profissional.id
        }

        response = self.client.post(self.url_listagem, dados_nova_consulta, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consulta.objects.count(), 2)

    def test_criar_consulta_sem_profissional_deve_falhar(self):
        """Garante que a API rejeita a criação de consulta sem vínculo a um profissional"""
        dados_incompletos = {
            "data": "2026-09-01T10:00:00Z"
        }

        response = self.client.post(self.url_listagem, dados_incompletos, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('profissional', response.data)

    def test_criar_consulta_profissional_inexistente_deve_falhar(self):
        """Garante que a API rejeita consulta vinculada a um profissional que não existe"""
        dados_invalidos = {
            "data": "2026-09-01T10:00:00Z",
            "profissional": 9999
        }

        response = self.client.post(self.url_listagem, dados_invalidos, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_atualizar_consulta(self):
        """Garante que a API atualiza a data de uma consulta existente"""
        dados_atualizados = {
            "data": "2026-08-15T09:00:00Z",
            "profissional": self.profissional.id
        }

        response = self.client.put(self.url_detalhe, dados_atualizados, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.consulta_teste.refresh_from_db()
        self.assertEqual(self.consulta_teste.profissional_id, self.profissional.id)

    def test_excluir_consulta(self):
        """Garante que a API remove uma consulta existente"""
        response = self.client.delete(self.url_detalhe)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consulta.objects.count(), 0)

    def test_buscar_consultas_por_profissional(self):
        """Garante que o filtro por profissional_id retorna só as consultas do profissional"""
        Consulta.objects.create(
            data="2026-09-05T11:00:00Z",
            profissional=self.outro_profissional
        )

        response = self.client.get(self.url_listagem, {'profissional_id': self.profissional.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['profissional'], self.profissional.id)

    def test_acesso_sem_token_deve_falhar(self):
        """Garante que a API bloqueia acesso sem autenticação"""
        self.client.credentials()
        response = self.client.get(self.url_listagem)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
