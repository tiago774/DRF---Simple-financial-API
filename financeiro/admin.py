from django.contrib import admin

from financeiro.models import Cliente, Conta, Transacao

class ClientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'cpf_cnpj', 'tipo_pessoa', 'ativo')
    list_display_links = ('id', 'nome')
    list_filter = ('tipo_pessoa', 'ativo')
    list_per_page = 20
    search_fields = ('nome', 'cpf_cnpj', 'email')

class ContasAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'cliente', 'tipo_conta', 'saldo', 'ativa')
    list_display_links = ('id', 'numero')
    list_filter = ('tipo_conta', 'ativa')
    search_fields = ('numero', 'agencia', 'cliente__nome')
    readonly_fields = ('saldo',)

class TransacoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'conta', 'tipo', 'valor', 'data_transacao')
    list_display_links = ('id',)
    list_filter = ('tipo', 'data_transacao')
    search_fields = ('conta__numero', 'descricao')
    readonly_fields = ('data_transacao',)

admin.site.register(Cliente, ClientesAdmin)
admin.site.register(Conta, ContasAdmin)
admin.site.register(Transacao, TransacoesAdmin)