from rest_framework import viewsets
from .models import Profissional, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer

class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultaSerializer

    def get_queryset(self):
        queryset = Consulta.objects.all()

        profissional_id = self.request.query_params.get('profissional_id')

        if profissional_id is not None:
            queryset = queryset.filter(profissional_id=profissional_id)

        return queryset
