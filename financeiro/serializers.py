from rest_framework import serializers
from financeiro.models import Cliente, Conta, Transacao
from financeiro.validators import cpf_cnpj_invalido, nome_invalido, telefone_invalido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'cpf_cnpj', 'tipo_pessoa', 'telefone', 'ativo']
        read_only_fields = ['data_cadastro']
    
    def validate(self, dados):
        # Validar CPF/CNPJ
        cpf_cnpj = dados.get('cpf_cnpj', '')
        if cpf_cnpj_invalido(cpf_cnpj):
            raise serializers.ValidationError({
                'cpf_cnpj': 'CPF/CNPJ inválido. Verifique o número informado.'
            })
        
        # Validar nome
        nome = dados.get('nome', '')
        if nome_invalido(nome):
            raise serializers.ValidationError({
                'nome': 'O nome deve conter apenas letras e espaços.'
            })
        
        # Validar telefone
        telefone = dados.get('telefone', '')
        if telefone_invalido(telefone):
            raise serializers.ValidationError({
                'telefone': 'Telefone deve estar no formato (XX) XXXXX-XXXX'
            })
        
        return dados


class ContaSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.ReadOnlyField(source='cliente.nome')
    cliente_cpf_cnpj = serializers.ReadOnlyField(source='cliente.cpf_cnpj')
    
    class Meta:
        model = Conta
        fields = ['id', 'cliente', 'cliente_nome', 'cliente_cpf_cnpj', 'numero', 
                 'agencia', 'tipo_conta', 'saldo', 'ativa']
        read_only_fields = ['data_abertura', 'saldo']


class TransacaoSerializer(serializers.ModelSerializer):
    conta_numero = serializers.ReadOnlyField(source='conta.numero')
    tipo_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Transacao
        fields = ['id', 'conta', 'conta_numero', 'tipo', 'tipo_display', 
                 'valor', 'descricao', 'data_transacao']
        read_only_fields = ['data_transacao']
    
    def get_tipo_display(self, obj):
        return obj.get_tipo_display()
    
    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError('O valor da transação deve ser positivo.')
        return value
    
    def validate(self, dados):
        # Validação de saldo para saques e pagamentos
        if dados.get('tipo') in ['S', 'P']:
            conta = dados.get('conta')
            if conta and conta.saldo < dados.get('valor', 0):
                raise serializers.ValidationError({
                    'valor': f'Saldo insuficiente. Saldo atual: R$ {conta.saldo:.2f}'
                })
        return dados


# Versão 2 dos serializers
class ClienteSerializerV2(serializers.ModelSerializer):
    tipo_pessoa_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'tipo_pessoa', 'tipo_pessoa_display', 
                 'data_cadastro', 'ativo']
    
    def get_tipo_pessoa_display(self, obj):
        return obj.get_tipo_pessoa_display()


class ContaSerializerV2(serializers.ModelSerializer):
    cliente_resumo = serializers.SerializerMethodField()
    saldo_formatado = serializers.SerializerMethodField()
    tipo_conta_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Conta
        fields = ['id', 'cliente_resumo', 'numero', 'agencia', 'tipo_conta', 
                 'tipo_conta_display', 'saldo_formatado', 'data_abertura']
    
    def get_cliente_resumo(self, obj):
        return {
            'id': obj.cliente.id,
            'nome': obj.cliente.nome,
            'tipo': obj.cliente.get_tipo_pessoa_display()
        }
    
    def get_saldo_formatado(self, obj):
        return f"R$ {obj.saldo:,.2f}"
    
    def get_tipo_conta_display(self, obj):
        return obj.get_tipo_conta_display()
