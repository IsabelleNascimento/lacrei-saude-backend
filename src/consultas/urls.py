from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet, ConsultaViewSet

router = DefaultRouter()
router.register(r'profissionais', ProfissionalViewSet, basename='profissional')
router.register(r'consultas', ConsultaViewSet, basename='consulta')

urlpatterns = [
    path('', include(router.urls)),
]