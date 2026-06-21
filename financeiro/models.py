from django.db import models
from django.core.validators import MinLengthValidator

class Cliente(models.Model):
    TIPO_PESSOA = (
        ('F', 'Física'),
        ('J', 'Jurídica'),
    )
    
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    tipo_pessoa = models.CharField(max_length=1, choices=TIPO_PESSOA, default='F')
    data_cadastro = models.DateField(auto_now_add=True)
    telefone = models.CharField(max_length=15)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome  # <-- CORREÇÃO: adicionar este método

class Conta(models.Model):
    TIPO_CONTA = (
        ('CC', 'Conta Corrente'),
        ('CP', 'Conta Poupança'),
        ('CI', 'Conta Investimento'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contas')
    numero = models.CharField(max_length=10, unique=True)
    agencia = models.CharField(max_length=6)
    tipo_conta = models.CharField(max_length=2, choices=TIPO_CONTA, default='CC')
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    data_abertura = models.DateField(auto_now_add=True)
    ativa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"

class Transacao(models.Model):
    TIPO_TRANSACAO = (
        ('D', 'Depósito'),
        ('S', 'Saque'),
        ('T', 'Transferência'),
        ('P', 'Pagamento'),
    )
    
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes')
    tipo = models.CharField(max_length=1, choices=TIPO_TRANSACAO)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    descricao = models.CharField(max_length=200, blank=True)
    data_transacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor:.2f}"
