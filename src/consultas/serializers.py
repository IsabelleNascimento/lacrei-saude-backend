from rest_framework import serializers
from .models import Profissional, Consulta

class ProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = ['id', 'nome_social', 'profissao', 'endereco', 'contato']


class ConsultaSerializer(serializers.ModelSerializer):
    profissional_nome = serializers.ReadOnlyField(source='profissional.nome_social')

    class Meta:
        model = Consulta
        fields = ['id', 'data', 'profissional', 'profissional_nome']
