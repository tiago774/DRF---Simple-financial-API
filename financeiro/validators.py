import re
from validate_docbr import CPF, CNPJ

def cpf_cnpj_invalido(numero):
    """Valida se é CPF ou CNPJ válido"""
    if not numero:
        return True
    
    # Remover caracteres especiais
    numero = re.sub(r'[^0-9]', '', numero)
    
    # Verificar se é CPF (11 dígitos) ou CNPJ (14 dígitos)
    if len(numero) == 11:
        cpf = CPF()
        return not cpf.validate(numero)
    elif len(numero) == 14:
        cnpj = CNPJ()
        return not cnpj.validate(numero)
    
    # Se não for nem 11 nem 14 dígitos, é inválido
    return True

def nome_invalido(nome):
    """Valida se o nome contém apenas letras e espaços"""
    if not nome:
        return True
    # Permitir letras, espaços, acentos e ç
    return not all(c.isalpha() or c.isspace() for c in nome)

def telefone_invalido(telefone):
    """Valida formato do telefone (XX) XXXXX-XXXX"""
    if not telefone:
        return True
    # Formato: (XX) XXXXX-XXXX
    modelo = r'^\([0-9]{2}\) [0-9]{5}-[0-9]{4}$'
    return not bool(re.match(modelo, telefone))
