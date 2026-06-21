from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from financeiro.models import Cliente, Conta, Transacao
from financeiro.serializers import ClienteSerializer

# CPFs válidos diferentes para cada teste
CPF_1 = '529.982.247-25'  # CPF válido
CPF_2 = '111.444.777-35'  # CPF válido
CPF_3 = '123.456.789-09'  # CPF válido

# Testes de Modelos
class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='João Teste',
            email='joao@teste.com',
            cpf_cnpj=CPF_1,
            tipo_pessoa='F',
            telefone='(11) 99999-9999'
        )
    
    def test_str_method(self):
        self.assertEqual(str(self.cliente), 'João Teste')
    
    def test_campos_obrigatorios(self):
        self.assertEqual(self.cliente.nome, 'João Teste')
        self.assertTrue(self.cliente.ativo)

class ContaModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome='Maria Teste',
            email='maria@teste.com',
            cpf_cnpj=CPF_2,
            tipo_pessoa='F',
            telefone='(11) 88888-8888'
        )
        self.conta = Conta.objects.create(
            cliente=self.cliente,
            numero='12345-6',
            agencia='0001',
            tipo_conta='CC',
            saldo=1000.00
        )
    
    def test_str_method(self):
        self.assertEqual(str(self.conta), '12345-6 - Maria Teste')
    
    def test_saldo_inicial(self):
        self.assertEqual(self.conta.saldo, 1000.00)

# Testes de Serializers
class ClienteSerializerTest(TestCase):
    def setUp(self):
        self.cliente_data = {
            'nome': 'Teste Serializer',
            'email': 'teste@serializer.com',
            'cpf_cnpj': CPF_1,
            'tipo_pessoa': 'F',
            'telefone': '(11) 99999-9999'
        }
    
    def test_serializer_valid(self):
        serializer = ClienteSerializer(data=self.cliente_data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        
        cliente = serializer.save()
        self.assertEqual(cliente.nome, 'Teste Serializer')
    
    def test_cpf_invalido(self):
        self.cliente_data['cpf_cnpj'] = '111.111.111-11'
        serializer = ClienteSerializer(data=self.cliente_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cpf_cnpj', serializer.errors)

# Testes de Views
class ClienteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Criar cliente com CPF_1
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            email='cliente@teste.com',
            cpf_cnpj=CPF_1,  # CPF diferente do que será usado no teste
            tipo_pessoa='F',
            telefone='(11) 99999-9999'
        )
        self.url = reverse('Clientes-list')
    
    def test_listar_clientes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_criar_cliente(self):
        data = {
            'nome': 'Novo Cliente',
            'email': 'novo@cliente.com',
            'cpf_cnpj': CPF_2,  # CPF DIFERENTE do usado no setUp
            'tipo_pessoa': 'F',
            'telefone': '(11) 77777-7777'
        }
        response = self.client.post(self.url, data)
        
        # DEBUG: Mostrar o erro se falhar
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Erro ao criar cliente: {response.data}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

class ContaViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.cliente = Cliente.objects.create(
            nome='Cliente Conta',
            email='conta@teste.com',
            cpf_cnpj=CPF_3,
            tipo_pessoa='F',
            telefone='(11) 99999-9999'
        )
        
        self.conta = Conta.objects.create(
            cliente=self.cliente,
            numero='12345-6',
            agencia='0001',
            tipo_conta='CC',
            saldo=1000.00
        )
        
        self.url = reverse('Contas-list')
    
    def test_listar_contas(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_criar_conta(self):
        data = {
            'cliente': self.cliente.id,
            'numero': '98765-4',
            'agencia': '0002',
            'tipo_conta': 'CP'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conta.objects.count(), 2)

# Testes de Autenticação
class AuthenticationUserTestCase(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_superuser(
            username='admin', 
            password='admin'
        )
        self.url = reverse('Clientes-list')
    
    def test_autenticacao_user_com_credenciais_corretas(self):
        from django.contrib.auth import authenticate
        user = authenticate(username='admin', password='admin')
        self.assertTrue((user is not None) and user.is_authenticated)
    
    def test_requisicao_get_nao_autorizada(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
