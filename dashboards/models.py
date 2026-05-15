from django.db import models
from django.core.exceptions import ValidationError


##----------------------------------------------------------------
###MODELO DE CONTAS A PAGAR###
##----------------------------------------------------------------

class ContaPagar(models.Model):
    codigo_lancamento_omie = models.BigIntegerField(
        unique=True,
        verbose_name="Código do lançamento Omie"
    )
    codigo_cliente_fornecedor = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="Código do cliente/fornecedor"
    )
    codigo_categoria = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Código da categoria"
    )
    codigo_tipo_documento = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código do tipo de documento"
    )

    chave_nfe = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Chave NFe"
    )
    numero_documento_fiscal = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número do documento fiscal"
    )
    numero_parcela = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Número da parcela"
    )
    numero_pedido = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Número do pedido"
    )

    id_conta_corrente = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="ID da conta corrente"
    )
    id_origem = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Origem"
    )
    operacao = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Operação"
    )

    data_emissao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de emissão"
    )
    data_entrada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de entrada"
    )
    data_previsao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de previsão"
    )
    data_vencimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de vencimento"
    )

    status_titulo = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Status do título"
    )
    valor_documento = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valor do documento"
    )

    retem_cofins = models.CharField(max_length=1, blank=True, null=True)
    retem_csll = models.CharField(max_length=1, blank=True, null=True)
    retem_inss = models.CharField(max_length=1, blank=True, null=True)
    retem_ir = models.CharField(max_length=1, blank=True, null=True)
    retem_iss = models.CharField(max_length=1, blank=True, null=True)
    retem_pis = models.CharField(max_length=1, blank=True, null=True)

    info_cimpapi = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Importado pela API"
    )
    info_d_inc = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de inclusão"
    )
    info_h_inc = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de inclusão"
    )
    info_u_inc = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de inclusão"
    )
    info_d_alt = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de alteração"
    )
    info_h_alt = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de alteração"
    )
    info_u_alt = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de alteração"
    )

    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ["-data_vencimento", "-codigo_lancamento_omie"]

    def __str__(self):
        return f"{self.codigo_lancamento_omie} - {self.valor_documento}"

##------------------------------------------------------------------
### MODELO DE CATEGORIAS  ##
##------------------------------------------------------------------


class Categoria(models.Model):
    categoria_superior = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Categoria superior"
    )
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    codigo_dre = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código DRE"
    )
    conta_despesa = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Conta despesa"
    )
    conta_inativa = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Conta inativa"
    )
    conta_receita = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Conta receita"
    )
    definida_pelo_usuario = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Definida pelo usuário"
    )
    descricao = models.CharField(
        max_length=255,
        verbose_name="Descrição"
    )
    descricao_padrao = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Descrição padrão"
    )
    id_conta_contabil = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="ID conta contábil"
    )
    nao_exibir = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Não exibir"
    )
    natureza = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Natureza"
    )
    tag_conta_contabil = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Tag conta contábil"
    )
    tipo_categoria = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Tipo da categoria"
    )
    totalizadora = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Totalizadora"
    )
    transferencia = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Transferência"
    )

    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["codigo", "descricao"]

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

#----------------------------------------------------------------
#------------------------CLIENTES E FORNECEDORES----------------------------------------

class ClienteFornecedor(models.Model):
    codigo_omie = models.BigIntegerField(
        unique=True,
        verbose_name="Codigo do cliente/fornecedor no Omie"
    )
    codigo_integracao = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Codigo de integracao"
    )
    razao_social = models.CharField(
        max_length=120,
        verbose_name="Razao social"
    )
    nome_fantasia = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Nome fantasia"
    )
    cnpj_cpf = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="CNPJ/CPF"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importacao"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Cliente/Fornecedor"
        verbose_name_plural = "Clientes/Fornecedores"
        ordering = ["nome_fantasia", "razao_social", "codigo_omie"]

    def __str__(self):
        return self.nome_fantasia or self.razao_social


##------------------------------------------------------------------
### MODELO DE CONTAS CORRENTES ##
##------------------------------------------------------------------

class ContaCorrente(models.Model):
    nCodCC = models.BigIntegerField(
        unique=True,
        verbose_name="Código da conta corrente Omie"
    )

    descricao = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Descrição"
    )

    codigo_banco = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código do banco"
    )
    codigo_agencia = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código da agência"
    )
    numero_conta_corrente = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número da conta corrente"
    )
    tipo = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Tipo"
    )
    tipo_conta_corrente = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Tipo da conta corrente"
    )
    modalidade = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Modalidade"
    )

    bloqueado = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Bloqueado"
    )
    inativo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Inativo"
    )
    importado_api = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Importado via API"
    )
    nao_fluxo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Não considerar no fluxo"
    )
    nao_resumo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Não considerar no resumo"
    )
    pix_sn = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Pix"
    )

    saldo_inicial = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Saldo inicial"
    )
    saldo_data = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Data do saldo"
    )
    valor_limite = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valor limite"
    )

    per_juros = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Percentual de juros"
    )
    per_multa = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Percentual de multa"
    )

    bol_sn = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Usa boleto"
    )
    bol_instr1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Instrução boleto 1"
    )
    bol_instr2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Instrução boleto 2"
    )
    bol_instr3 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Instrução boleto 3"
    )
    bol_instr4 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Instrução boleto 4"
    )
    cancinstr = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Cancelamento instrução"
    )

    cobr_sn = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Cobrança"
    )
    cobr_esp = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Espécie de cobrança"
    )
    cnab_esp = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Espécie CNAB"
    )

    pdv_bandeira = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Bandeira PDV"
    )
    pdv_categoria = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Categoria PDV"
    )
    pdv_cod_adm = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Código administradora PDV"
    )
    pdv_dias_venc = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Dias vencimento PDV"
    )
    pdv_enviar = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Enviar PDV"
    )
    pdv_limite_pacelas = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Limite parcelas PDV"
    )
    pdv_num_parcelas = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Número parcelas PDV"
    )
    pdv_sincr_analitica = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Sincronização analítica PDV"
    )
    pdv_taxa_adm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Taxa administradora PDV"
    )
    pdv_taxa_loja = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Taxa loja PDV"
    )
    pdv_tipo_tef = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Tipo TEF PDV"
    )

    cCnpjInstFinanc = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="CNPJ instituição financeira"
    )
    cCodCCInt = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Código interno da conta"
    )
    cEstabelecimento = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Estabelecimento"
    )
    cTipoCartao = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Tipo do cartão"
    )

    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Endereço"
    )
    numero = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Número"
    )
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento"
    )
    bairro = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Bairro"
    )
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name="Estado"
    )
    cep = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="CEP"
    )
    codigo_pais = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Código do país"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="E-mail"
    )
    ddd = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name="DDD"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    nome_gerente = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nome do gerente"
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observação"
    )

    dias_rcomp = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Dias recomp"
    )

    data_inc = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de inclusão"
    )
    hora_inc = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de inclusão"
    )
    user_inc = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de inclusão"
    )
    data_alt = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de alteração"
    )
    hora_alt = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de alteração"
    )
    user_alt = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de alteração"
    )

    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Conta Corrente"
        verbose_name_plural = "Contas Correntes"
        ordering = ["descricao", "nCodCC"]

    def __str__(self):
        return f"{self.nCodCC} - {self.descricao}"



##------------------------------------------------------------------
### MODELO DE PARÂMETROS POR EMPRESA ##
##------------------------------------------------------------------

class ProjetoOmie(models.Model):
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Codigo do projeto na Omie"
    )
    codigo_integracao = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Codigo de integracao"
    )
    nome = models.CharField(
        max_length=150,
        verbose_name="Nome do projeto"
    )
    inativo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Inativo"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importacao"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Projeto Omie"
        verbose_name_plural = "Projetos Omie"
        ordering = ["nome", "codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class EmpresaOmie(models.Model):
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Codigo da empresa na Omie"
    )
    nome_fantasia = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nome fantasia"
    )
    razao_social = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Razao social"
    )
    cnpj_cpf = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="CNPJ/CPF"
    )
    inativo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Inativo"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importacao"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Empresa Omie"
        verbose_name_plural = "Empresas Omie"
        ordering = ["nome_fantasia", "razao_social", "codigo"]

    def __str__(self):
        return self.nome_fantasia or self.razao_social or self.codigo


class DepartamentoOmie(models.Model):
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Codigo do departamento na Omie"
    )
    codigo_superior = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Codigo do departamento superior"
    )
    descricao = models.CharField(
        max_length=150,
        verbose_name="Descricao"
    )
    inativo = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Inativo"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importacao"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Departamento Omie"
        verbose_name_plural = "Departamentos Omie"
        ordering = ["descricao", "codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class TipoContaCorrenteOmie(models.Model):
    codigo = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Codigo do tipo de conta corrente na Omie"
    )
    descricao = models.CharField(
        max_length=150,
        verbose_name="Descricao"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importacao"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Tipo de Conta Corrente Omie"
        verbose_name_plural = "Tipos de Conta Corrente Omie"
        ordering = ["descricao", "codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class ParametroEmpresa(models.Model):
    slug_empresa = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug da empresa"
    )
    nome_empresa = models.CharField(
        max_length=150,
        verbose_name="Nome da empresa"
    )

    app_key_omie = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="App Key Omie"
        )

    app_secret_omie = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="App Secret Omie"
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação"
    )

    class Meta:
        verbose_name = "Parâmetro da Empresa"
        verbose_name_plural = "Parâmetros das Empresas"
        ordering = ["nome_empresa"]

    def __str__(self):
        return self.nome_empresa



##------------------------------------------------------------------
### MODELO DE CONTAS A RECEBER ##
##------------------------------------------------------------------

class ContaReceber(models.Model):
    codigo_lancamento_omie = models.BigIntegerField(
        unique=True,
        verbose_name="Código do lançamento Omie"
    )
    codigo_cliente_fornecedor = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="Código do cliente/fornecedor"
    )
    codigo_categoria = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Código da categoria"
    )
    codigo_lancamento_integracao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Código do lançamento integração"
    )
    codigo_tipo_documento = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código do tipo de documento"
    )

    chave_nfe = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name="Chave NFe"
    )
    numero_documento_fiscal = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número do documento fiscal"
    )
    numero_parcela = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Número da parcela"
    )
    numero_pedido = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Número do pedido"
    )
    nCodPedido = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="Código do pedido"
    )

    id_conta_corrente = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="ID da conta corrente"
    )
    id_origem = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Origem"
    )
    operacao = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Operação"
    )
    tipo_agrupamento = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Tipo de agrupamento"
    )

    data_emissao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de emissão"
    )
    data_previsao = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de previsão"
    )
    data_registro = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de registro"
    )
    data_vencimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de vencimento"
    )

    status_titulo = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Status do título"
    )
    valor_documento = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valor do documento"
    )

    retem_cofins = models.CharField(max_length=1, blank=True, null=True)
    retem_csll = models.CharField(max_length=1, blank=True, null=True)
    retem_inss = models.CharField(max_length=1, blank=True, null=True)
    retem_ir = models.CharField(max_length=1, blank=True, null=True)
    retem_iss = models.CharField(max_length=1, blank=True, null=True)
    retem_pis = models.CharField(max_length=1, blank=True, null=True)

    boleto_cGerado = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Boleto gerado"
    )
    boleto_cNumBancario = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número bancário do boleto"
    )
    boleto_cNumBoleto = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número do boleto"
    )
    boleto_dDtEmBol = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de emissão do boleto"
    )
    boleto_nPerJuros = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Percentual de juros do boleto"
    )
    boleto_nPerMulta = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Percentual de multa do boleto"
    )

    info_cimpapi = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="Importado pela API"
    )
    info_d_inc = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de inclusão"
    )
    info_h_inc = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de inclusão"
    )
    info_u_inc = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de inclusão"
    )
    info_d_alt = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de alteração"
    )
    info_h_alt = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Hora de alteração"
    )
    info_u_alt = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Usuário de alteração"
    )

    data_importacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de importação"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ["-data_vencimento", "-codigo_lancamento_omie"]

    def __str__(self):
        return f"{self.codigo_lancamento_omie} - {self.valor_documento}"


##------------------------------------------------------------------
### MODELO DE CONTAS DO DRE ##
##------------------------------------------------------------------
class ContaDRE(models.Model):
    SINAL_CHOICES = [
        ('positivo', 'Positivo (+)'),
        ('negativo', 'Negativo (-)'),
        ('resultado', 'Resultado (=)'),
    ]

    nome = models.CharField(
        max_length=150,
        verbose_name='Nome da conta'
    )

    pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='filhos',
        verbose_name='Conta pai'
    )

    nivel = models.PositiveSmallIntegerField(
        editable=False,
        verbose_name='Nível'
    )

    sinal = models.CharField(
        max_length=10,
        choices=SINAL_CHOICES,
        null=True,
        blank=True,
        verbose_name='Sinal'
    )

    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )

    kpi = models.BooleanField(
        default=False,
        verbose_name='KPI'
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Conta DRE'
        verbose_name_plural = 'Contas DRE'
        ordering = ['nivel', 'ordem', 'nome']

    def __str__(self):
        return self.nome

    def clean(self):
        if self.pai and self.pai == self:
            raise ValidationError({'pai': 'Uma conta não pode ser pai dela mesma.'})

        if self.pai is None:
            self.nivel = 1
        else:
            if self.pai.nivel >= 2:
                raise ValidationError({'pai': 'Só é permitido até 2 níveis (pai e filho).'})
            self.nivel = 2

        if self.pk and self.pai:
            ancestral = self.pai
            while ancestral:
                if ancestral == self:
                    raise ValidationError({'pai': 'Referência circular detectada.'})
                ancestral = ancestral.pai

            def save(self, *args, **kwargs):
                self.full_clean()
                super().save(*args, **kwargs)

#--------------------------------------------------------------------------------------
#DE-PARA DRE 
#---------------------------------------------------------------------------------

class DeParaCategoriaDRE(models.Model):
    empresa = models.ForeignKey(
        ParametroEmpresa,
        on_delete=models.CASCADE,
        related_name='deparas_dre',
        verbose_name="Empresa"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='deparas_dre',
        verbose_name="Categoria"
    )
    conta_dre = models.ForeignKey(
        ContaDRE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categorias_vinculadas',
        verbose_name="Conta DRE"
    )

#--------------------------------------------------------------------------------------
#DE-PARA DRE 
#---------------------------------------------------------------------------------

class ComposicaoContaDRE(models.Model):
    conta_resultado = models.ForeignKey(
        'ContaDRE',
        on_delete=models.CASCADE,
        related_name='componentes_formula',
        verbose_name='Conta de resultado'
    )
    conta_origem = models.ForeignKey(
        'ContaDRE',
        on_delete=models.CASCADE,
        related_name='participa_de_formulas',
        verbose_name='Conta de origem'
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )

    class Meta:
        verbose_name = 'Composição da Conta DRE'
        verbose_name_plural = 'Composições das Contas DRE'
        ordering = ['ordem', 'id']

    def __str__(self):
        return f'{self.conta_resultado} <= {self.conta_origem}'


class IndicadorConfiguracao(models.Model):
    CHAVE_CHOICES = [
        ('receita_bruta', 'Receita Bruta'),
        ('deducoes_gastos_variaveis', 'Deducoes e Gastos Variaveis'),
        ('margem_contribuicao', 'Margem de Contribuicao'),
        ('gastos_fixos', 'Gastos Fixos'),
        ('ebit', 'EBIT'),
    ]

    empresa = models.ForeignKey(
        ParametroEmpresa,
        on_delete=models.CASCADE,
        related_name='indicadores_configurados',
        verbose_name='Empresa',
    )
    chave = models.CharField(
        max_length=50,
        choices=CHAVE_CHOICES,
        verbose_name='Indicador',
    )
    conta_1 = models.ForeignKey(
        ContaDRE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='indicador_como_conta_1',
        verbose_name='Conta 1',
    )
    conta_2 = models.ForeignKey(
        ContaDRE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='indicador_como_conta_2',
        verbose_name='Conta 2',
    )
    conta_3 = models.ForeignKey(
        ContaDRE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='indicador_como_conta_3',
        verbose_name='Conta 3',
    )
    conta_4 = models.ForeignKey(
        ContaDRE,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='indicador_como_conta_4',
        verbose_name='Conta 4',
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuracao de Indicador'
        verbose_name_plural = 'Configuracoes de Indicadores'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'chave'],
                name='uniq_indicador_config_empresa_chave',
            ),
        ]

    def __str__(self):
        return f'{self.empresa} - {self.get_chave_display()}'


class DREProjetado(models.Model):
    TIPO_LINHA_CHOICES = [
        ('conta', 'Conta DRE'),
        ('categoria', 'Categoria'),
    ]

    empresa = models.ForeignKey(
        ParametroEmpresa,
        on_delete=models.CASCADE,
        related_name='projetados_dre',
        verbose_name='Empresa',
    )
    conta_dre = models.ForeignKey(
        ContaDRE,
        on_delete=models.CASCADE,
        related_name='projetados',
        verbose_name='Conta DRE',
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='projetados_dre',
        verbose_name='Categoria',
    )
    tipo_linha = models.CharField(
        max_length=10,
        choices=TIPO_LINHA_CHOICES,
        verbose_name='Tipo de linha',
    )
    ano = models.PositiveSmallIntegerField(verbose_name='Ano')
    mes = models.PositiveSmallIntegerField(verbose_name='Mes')
    valor = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name='Valor projetado',
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DRE Projetado'
        verbose_name_plural = 'DRE Projetado'
        constraints = [
            models.UniqueConstraint(
                fields=['empresa', 'tipo_linha', 'conta_dre', 'categoria', 'ano', 'mes'],
                name='uniq_dre_projetado_linha_mes',
            ),
        ]
        ordering = ['ano', 'mes', 'conta_dre__ordem', 'categoria__codigo']

    def __str__(self):
        return f'{self.empresa} - {self.ano}/{self.mes:02d} - {self.conta_dre} - {self.valor}'
