from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from financeiro.models import Cliente, Conta, Transacao
from financeiro.serializers import (
    ClienteSerializer, ClienteSerializerV2,
    ContaSerializer, ContaSerializerV2,
    TransacaoSerializer
)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome', 'data_cadastro']
    search_fields = ['nome', 'cpf_cnpj', 'email']
    
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ClienteSerializerV2
        return ClienteSerializer


class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cliente', 'tipo_conta', 'ativa']
    ordering_fields = ['numero', 'saldo']
    http_method_names = ['get', 'post', 'put']  # DELETE não permitido
    
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ContaSerializerV2
        return ContaSerializer


class TransacaoViewSet(viewsets.ModelViewSet):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['conta', 'tipo']
    ordering_fields = ['data_transacao', 'valor']
    http_method_names = ['get', 'post']  # Apenas listar e criar
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Processar transação
        transacao = serializer.save()
        conta = transacao.conta
        
        # Atualizar saldo da conta
        if transacao.tipo in ['D']:  # Depósito
            conta.saldo += transacao.valor
        elif transacao.tipo in ['S', 'P']:  # Saque ou Pagamento
            conta.saldo -= transacao.valor
        # Transferências precisariam de lógica adicional com duas contas
        
        conta.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Views para listagens personalizadas
class ExtratoContaView(generics.ListAPIView):
    serializer_class = TransacaoSerializer
    
    def get_queryset(self):
        return Transacao.objects.filter(conta_id=self.kwargs['pk']).order_by('-data_transacao')


class ContasClienteView(generics.ListAPIView):
    serializer_class = ContaSerializer
    
    def get_queryset(self):
        return Conta.objects.filter(cliente_id=self.kwargs['pk'], ativa=True)