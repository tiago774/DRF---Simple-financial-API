from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from financeiro.views import (
    ClienteViewSet, ContaViewSet, TransacaoViewSet,
    ExtratoContaView, ContasClienteView
)

router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='Clientes')
router.register('contas', ContaViewSet, basename='Contas')
router.register('transacoes', TransacaoViewSet, basename='Transacoes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('clientes/<int:pk>/contas/', ContasClienteView.as_view()),
    path('contas/<int:pk>/extrato/', ExtratoContaView.as_view()),
]