import html
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Dict, List

import requests

from .models import Categoria, ClienteFornecedor, ContaCorrente, ContaPagar, ContaReceber

OMIE_CATEGORIAS_URL = "https://app.omie.com.br/api/v1/geral/categorias/"
OMIE_CLIENTES_URL = "https://app.omie.com.br/api/v1/geral/clientes/"
OMIE_CONTAS_CORRENTES_URL = "https://app.omie.com.br/api/v1/geral/contacorrente/"
OMIE_CONTAS_PAGAR_URL = "https://app.omie.com.br/api/v1/financas/contapagar/"
OMIE_CONTAS_RECEBER_URL = "https://app.omie.com.br/api/v1/financas/contareceber/"
TOTAL_ETAPAS_SINCRONIZACAO = 5


def chave_ordenacao_categoria(codigo: str):
    if not codigo:
        return ()
    try:
        return tuple(int(parte) for parte in codigo.split("."))
    except ValueError:
        return (codigo,)


def limpar_texto(texto):
    if not texto:
        return ""
    texto = html.unescape(str(texto)).strip()
    if texto.lower() in {"<disponã­vel>", "<disponível>"}:
        return ""
    return texto


def _parse_date(valor):
    if not valor:
        return None

    valor = str(valor).strip()
    if not valor:
        return None

    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            from datetime import datetime

            return datetime.strptime(valor, formato).date()
        except ValueError:
            continue

    return None


def _parse_decimal(valor):
    if valor in (None, ""):
        return None

    if isinstance(valor, Decimal):
        return valor

    texto = str(valor).strip()
    if not texto:
        return None

    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")

    try:
        return Decimal(texto)
    except (InvalidOperation, ValueError):
        return None


def _parse_int(valor):
    if valor in (None, ""):
        return None

    try:
        return int(str(valor).strip())
    except (TypeError, ValueError):
        return None


def _extrair_info(item, *chaves):
    if not isinstance(item, dict):
        return None

    for chave in chaves:
        valor = item.get(chave)
        if valor not in (None, ""):
            return valor
    return None


def _post_omie(url: str, call: str, app_key: str, app_secret: str, parametros: Dict[str, Any]):
    payload = {
        "call": call,
        "param": [parametros],
        "app_key": app_key,
        "app_secret": app_secret,
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    fault = data.get("faultstring") or data.get("faultcode")
    if fault:
        raise ValueError(fault)

    return data


def _emitir_progresso(callback: Callable[[Dict[str, Any]], None] | None, **payload):
    if callback:
        callback(payload)


def _calcular_percentual_etapa(indice_etapa: int, progresso_etapa: float, total_etapas: int = TOTAL_ETAPAS_SINCRONIZACAO) -> int:
    progresso_etapa = max(0.0, min(progresso_etapa, 1.0))
    percentual = ((indice_etapa - 1) + progresso_etapa) / total_etapas
    return int(percentual * 100)


def _listar_registros_paginados(
    *,
    url: str,
    call: str,
    app_key: str,
    app_secret: str,
    response_keys: List[str],
    registros_por_pagina: int = 500,
    parametros_extras: Dict[str, Any] | None = None,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
):
    pagina = 1
    registros: List[Dict[str, Any]] = []
    parametros_extras = parametros_extras or {}

    while True:
        parametros = {
            "pagina": pagina,
            "registros_por_pagina": registros_por_pagina,
            **parametros_extras,
        }
        data = _post_omie(url, call, app_key, app_secret, parametros)

        lote = []
        for chave in response_keys:
            lote = data.get(chave) or []
            if lote:
                break

        registros.extend(lote)

        total_de_paginas = _parse_int(data.get("total_de_paginas")) or 1
        total_de_registros = _parse_int(data.get("total_de_registros")) or len(registros)
        _emitir_progresso(
            progress_callback,
            pagina=pagina,
            total_paginas=total_de_paginas,
            registros_coletados=len(registros),
            total_registros=total_de_registros,
        )
        if pagina >= total_de_paginas:
            break

        pagina += 1

    return registros


def listar_categorias_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
) -> List[Dict[str, Any]]:
    categorias = _listar_registros_paginados(
        url=OMIE_CATEGORIAS_URL,
        call="ListarCategorias",
        app_key=app_key,
        app_secret=app_secret,
        response_keys=["categoria_cadastro", "categorias"],
        progress_callback=progress_callback,
    )
    categorias.sort(key=lambda item: chave_ordenacao_categoria(item.get("codigo", "")))
    return categorias


def importar_categorias_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
    indice_etapa: int = 1,
) -> int:
    _emitir_progresso(
        progress_callback,
        etapa="categorias",
        fase="buscando",
        mensagem="Buscando categorias na Omie...",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.02),
    )
    categorias = listar_categorias_omie(
        app_key,
        app_secret,
        progress_callback=lambda info: _emitir_progresso(
            progress_callback,
            etapa="categorias",
            fase="buscando",
            mensagem=(
                f"Buscando categorias na Omie "
                f"({info['pagina']}/{info['total_paginas']} paginas)..."
            ),
            percentual=_calcular_percentual_etapa(
                indice_etapa,
                0.05 + (0.35 * (info["pagina"] / max(info["total_paginas"], 1))),
            ),
        ),
    )
    total_processadas = 0
    codigos_ativos = set()
    total_categorias = len(categorias)

    _emitir_progresso(
        progress_callback,
        etapa="categorias",
        fase="gravando",
        mensagem=f"Gravando categorias no banco... (0/{total_categorias})",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.40 if total_categorias else 1.0),
    )

    for indice, item in enumerate(categorias, start=1):
        codigo = item.get("codigo")
        conta_inativa = (item.get("conta_inativa") or "").strip().upper()

        if conta_inativa == "S":
            if codigo:
                Categoria.objects.filter(codigo=codigo).delete()
            continue

        if not codigo:
            continue

        codigos_ativos.add(codigo)

        Categoria.objects.update_or_create(
            codigo=codigo,
            defaults={
                "categoria_superior": item.get("categoria_superior"),
                "codigo_dre": item.get("codigo_dre"),
                "conta_despesa": item.get("conta_despesa"),
                "conta_inativa": item.get("conta_inativa"),
                "conta_receita": item.get("conta_receita"),
                "definida_pelo_usuario": item.get("definida_pelo_usuario"),
                "descricao": limpar_texto(item.get("descricao")),
                "descricao_padrao": limpar_texto(item.get("descricao_padrao")),
                "id_conta_contabil": item.get("id_conta_contabil"),
                "nao_exibir": item.get("nao_exibir"),
                "natureza": item.get("natureza"),
                "tag_conta_contabil": item.get("tag_conta_contabil"),
                "tipo_categoria": item.get("tipo_categoria"),
                "totalizadora": item.get("totalizadora"),
                "transferencia": item.get("transferencia"),
            },
        )
        total_processadas += 1

        if total_categorias and (indice == total_categorias or indice % 25 == 0):
            _emitir_progresso(
                progress_callback,
                etapa="categorias",
                fase="gravando",
                mensagem=f"Gravando categorias no banco... ({indice}/{total_categorias})",
                percentual=_calcular_percentual_etapa(
                    indice_etapa,
                    0.40 + (0.60 * (indice / total_categorias)),
                ),
            )

    if codigos_ativos:
        Categoria.objects.exclude(codigo__in=codigos_ativos).delete()

    return total_processadas


def listar_clientes_fornecedores_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
) -> List[Dict[str, Any]]:
    clientes = _listar_registros_paginados(
        url=OMIE_CLIENTES_URL,
        call="ListarClientes",
        app_key=app_key,
        app_secret=app_secret,
        response_keys=["clientes_cadastro", "clientes_cadastro_resumido", "ListarClientes"],
        parametros_extras={"apenas_importado_api": "N"},
        progress_callback=progress_callback,
    )
    if not clientes:
        clientes = _listar_registros_paginados(
            url=OMIE_CLIENTES_URL,
            call="ListarClientesResumido",
            app_key=app_key,
            app_secret=app_secret,
            response_keys=["clientes_cadastro_resumido", "clientes_cadastro", "ListarClientesResumido"],
            parametros_extras={"apenas_importado_api": "N"},
            progress_callback=progress_callback,
        )
    clientes.sort(
        key=lambda item: (
            limpar_texto(item.get("nome_fantasia")),
            limpar_texto(item.get("razao_social")),
            item.get("codigo_cliente_omie") or 0,
        )
    )
    return clientes


def importar_clientes_fornecedores_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
    indice_etapa: int = 2,
) -> int:
    _emitir_progresso(
        progress_callback,
        etapa="clientes_fornecedores",
        fase="buscando",
        mensagem="Buscando clientes e fornecedores na Omie...",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.02),
    )
    clientes = listar_clientes_fornecedores_omie(
        app_key,
        app_secret,
        progress_callback=lambda info: _emitir_progresso(
            progress_callback,
            etapa="clientes_fornecedores",
            fase="buscando",
            mensagem=(
                f"Buscando clientes e fornecedores na Omie "
                f"({info['pagina']}/{info['total_paginas']} paginas)..."
            ),
            percentual=_calcular_percentual_etapa(
                indice_etapa,
                0.05 + (0.35 * (info["pagina"] / max(info["total_paginas"], 1))),
            ),
        ),
    )
    total_processados = 0
    codigos_ativos = set()
    total_clientes = len(clientes)

    _emitir_progresso(
        progress_callback,
        etapa="clientes_fornecedores",
        fase="gravando",
        mensagem=f"Gravando clientes e fornecedores no banco... (0/{total_clientes})",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.40 if total_clientes else 1.0),
    )

    for indice, item in enumerate(clientes, start=1):
        codigo_omie = _parse_int(item.get("codigo_cliente_omie"))
        if not codigo_omie:
            continue

        codigos_ativos.add(codigo_omie)

        nome_fantasia = limpar_texto(item.get("nome_fantasia"))
        razao_social = limpar_texto(item.get("razao_social")) or nome_fantasia or f"Cliente/Fornecedor {codigo_omie}"

        ClienteFornecedor.objects.update_or_create(
            codigo_omie=codigo_omie,
            defaults={
                "codigo_integracao": item.get("codigo_cliente_integracao"),
                "razao_social": razao_social,
                "nome_fantasia": nome_fantasia,
                "cnpj_cpf": item.get("cnpj_cpf"),
            },
        )
        total_processados += 1

        if total_clientes and (indice == total_clientes or indice % 25 == 0):
            _emitir_progresso(
                progress_callback,
                etapa="clientes_fornecedores",
                fase="gravando",
                mensagem=f"Gravando clientes e fornecedores no banco... ({indice}/{total_clientes})",
                percentual=_calcular_percentual_etapa(
                    indice_etapa,
                    0.40 + (0.60 * (indice / total_clientes)),
                ),
            )

    if codigos_ativos:
        ClienteFornecedor.objects.exclude(codigo_omie__in=codigos_ativos).delete()

    return total_processados


def listar_contas_correntes_omie(app_key: str, app_secret: str) -> List[Dict[str, Any]]:
    contas = _listar_registros_paginados(
        url=OMIE_CONTAS_CORRENTES_URL,
        call="ListarContasCorrentes",
        app_key=app_key,
        app_secret=app_secret,
        response_keys=["ListarContasCorrentes", "lista_contas_correntes", "conta_corrente_cadastro"],
        parametros_extras={"apenas_importado_api": "N"},
    )
    contas.sort(key=lambda item: (limpar_texto(item.get("descricao")), item.get("nCodCC") or 0))
    return contas


def importar_contas_correntes_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
    indice_etapa: int = 3,
) -> int:
    _emitir_progresso(
        progress_callback,
        etapa="contas_correntes",
        fase="buscando",
        mensagem="Buscando contas correntes na Omie...",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.02),
    )
    contas = listar_contas_correntes_omie(app_key, app_secret)
    total_processadas = 0
    codigos_ativos = set()
    total_contas = len(contas)

    _emitir_progresso(
        progress_callback,
        etapa="contas_correntes",
        fase="gravando",
        mensagem=f"Gravando contas correntes no banco... (0/{total_contas})",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.40 if total_contas else 1.0),
    )

    for indice, item in enumerate(contas, start=1):
        codigo = _parse_int(item.get("nCodCC"))
        if not codigo:
            continue

        codigos_ativos.add(codigo)

        ContaCorrente.objects.update_or_create(
            nCodCC=codigo,
            defaults={
                "descricao": limpar_texto(item.get("descricao")),
                "codigo_banco": item.get("codigo_banco"),
                "codigo_agencia": item.get("codigo_agencia"),
                "numero_conta_corrente": item.get("numero_conta_corrente"),
                "tipo": item.get("tipo"),
                "tipo_conta_corrente": item.get("tipo_conta_corrente"),
                "modalidade": item.get("modalidade"),
                "bloqueado": item.get("bloqueado"),
                "inativo": item.get("inativo"),
                "importado_api": item.get("importado_api"),
                "nao_fluxo": item.get("nao_fluxo"),
                "nao_resumo": item.get("nao_resumo"),
                "pix_sn": item.get("pix_sn"),
                "saldo_inicial": _parse_decimal(item.get("saldo_inicial")),
                "saldo_data": item.get("saldo_data"),
                "valor_limite": _parse_decimal(item.get("valor_limite")),
                "per_juros": _parse_decimal(item.get("per_juros")),
                "per_multa": _parse_decimal(item.get("per_multa")),
                "bol_sn": item.get("bol_sn"),
                "bol_instr1": limpar_texto(item.get("bol_instr1")),
                "bol_instr2": limpar_texto(item.get("bol_instr2")),
                "bol_instr3": limpar_texto(item.get("bol_instr3")),
                "bol_instr4": limpar_texto(item.get("bol_instr4")),
                "cancinstr": limpar_texto(item.get("cancinstr")),
                "cobr_sn": item.get("cobr_sn"),
                "cobr_esp": item.get("cobr_esp"),
                "cnab_esp": item.get("cnab_esp"),
                "pdv_bandeira": item.get("pdv_bandeira"),
                "pdv_categoria": item.get("pdv_categoria"),
                "pdv_cod_adm": _parse_int(item.get("pdv_cod_adm")),
                "pdv_dias_venc": _parse_int(item.get("pdv_dias_venc")),
                "pdv_enviar": item.get("pdv_enviar"),
                "pdv_limite_pacelas": _parse_int(item.get("pdv_limite_pacelas")),
                "pdv_num_parcelas": _parse_int(item.get("pdv_num_parcelas")),
                "pdv_sincr_analitica": item.get("pdv_sincr_analitica"),
                "pdv_taxa_adm": _parse_decimal(item.get("pdv_taxa_adm")),
                "pdv_taxa_loja": _parse_decimal(item.get("pdv_taxa_loja")),
                "pdv_tipo_tef": _parse_int(item.get("pdv_tipo_tef")),
                "cCnpjInstFinanc": item.get("cCnpjInstFinanc"),
                "cCodCCInt": item.get("cCodCCInt"),
                "cEstabelecimento": item.get("cEstabelecimento"),
                "cTipoCartao": item.get("cTipoCartao"),
                "endereco": limpar_texto(item.get("endereco")),
                "numero": item.get("numero"),
                "complemento": limpar_texto(item.get("complemento")),
                "bairro": limpar_texto(item.get("bairro")),
                "cidade": limpar_texto(item.get("cidade")),
                "estado": item.get("estado"),
                "cep": item.get("cep"),
                "codigo_pais": item.get("codigo_pais"),
                "email": item.get("email"),
                "ddd": item.get("ddd"),
                "telefone": item.get("telefone"),
                "nome_gerente": limpar_texto(item.get("nome_gerente")),
                "observacao": limpar_texto(item.get("observacao")),
                "dias_rcomp": _parse_int(item.get("dias_rcomp")),
                "data_inc": _parse_date(item.get("data_inc")),
                "hora_inc": item.get("hora_inc"),
                "user_inc": item.get("user_inc"),
                "data_alt": _parse_date(item.get("data_alt")),
                "hora_alt": item.get("hora_alt"),
                "user_alt": item.get("user_alt"),
            },
        )
        total_processadas += 1

        if total_contas and (indice == total_contas or indice % 25 == 0):
            _emitir_progresso(
                progress_callback,
                etapa="contas_correntes",
                fase="gravando",
                mensagem=f"Gravando contas correntes no banco... ({indice}/{total_contas})",
                percentual=_calcular_percentual_etapa(
                    indice_etapa,
                    0.40 + (0.60 * (indice / total_contas)),
                ),
            )

    if codigos_ativos:
        ContaCorrente.objects.exclude(nCodCC__in=codigos_ativos).delete()

    return total_processadas


def listar_contas_pagar_omie(app_key: str, app_secret: str) -> List[Dict[str, Any]]:
    contas = _listar_registros_paginados(
        url=OMIE_CONTAS_PAGAR_URL,
        call="ListarContasPagar",
        app_key=app_key,
        app_secret=app_secret,
        response_keys=["conta_pagar_cadastro", "titulosEncontrados", "lista_contas_pagar"],
        parametros_extras={"apenas_importado_api": "N"},
    )
    contas.sort(key=lambda item: (item.get("data_vencimento") or "", item.get("codigo_lancamento_omie") or 0))
    return contas


def importar_contas_pagar_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
    indice_etapa: int = 4,
) -> int:
    _emitir_progresso(
        progress_callback,
        etapa="contas_pagar",
        fase="buscando",
        mensagem="Buscando contas a pagar na Omie...",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.02),
    )
    contas = listar_contas_pagar_omie(app_key, app_secret)
    total_processadas = 0
    codigos_ativos = set()
    total_contas = len(contas)

    _emitir_progresso(
        progress_callback,
        etapa="contas_pagar",
        fase="gravando",
        mensagem=f"Gravando contas a pagar no banco... (0/{total_contas})",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.40 if total_contas else 1.0),
    )

    for indice, item in enumerate(contas, start=1):
        codigo = _parse_int(_extrair_info(item, "codigo_lancamento_omie", "nCodTitulo"))
        if not codigo:
            continue

        codigos_ativos.add(codigo)
        info = item.get("info") if isinstance(item.get("info"), dict) else {}

        ContaPagar.objects.update_or_create(
            codigo_lancamento_omie=codigo,
            defaults={
                "codigo_cliente_fornecedor": _parse_int(_extrair_info(item, "codigo_cliente_fornecedor", "codigo_cliente_omie")),
                "codigo_categoria": _extrair_info(item, "codigo_categoria"),
                "codigo_tipo_documento": _extrair_info(item, "codigo_tipo_documento"),
                "chave_nfe": _extrair_info(item, "chave_nfe"),
                "numero_documento_fiscal": _extrair_info(item, "numero_documento_fiscal"),
                "numero_parcela": _extrair_info(item, "numero_parcela"),
                "numero_pedido": _extrair_info(item, "numero_pedido"),
                "id_conta_corrente": _parse_int(_extrair_info(item, "id_conta_corrente", "nCodCC")),
                "id_origem": _extrair_info(item, "id_origem"),
                "operacao": _extrair_info(item, "operacao"),
                "data_emissao": _parse_date(_extrair_info(item, "data_emissao")),
                "data_entrada": _parse_date(_extrair_info(item, "data_entrada")),
                "data_previsao": _parse_date(_extrair_info(item, "data_previsao")),
                "data_vencimento": _parse_date(_extrair_info(item, "data_vencimento")),
                "status_titulo": _extrair_info(item, "status_titulo"),
                "valor_documento": _parse_decimal(_extrair_info(item, "valor_documento")),
                "retem_cofins": _extrair_info(item, "retem_cofins"),
                "retem_csll": _extrair_info(item, "retem_csll"),
                "retem_inss": _extrair_info(item, "retem_inss"),
                "retem_ir": _extrair_info(item, "retem_ir"),
                "retem_iss": _extrair_info(item, "retem_iss"),
                "retem_pis": _extrair_info(item, "retem_pis"),
                "info_cimpapi": _extrair_info(info, "cImpAPI", "info_cimpapi"),
                "info_d_inc": _parse_date(_extrair_info(info, "dInc", "info_d_inc")),
                "info_h_inc": _extrair_info(info, "hInc", "info_h_inc"),
                "info_u_inc": _extrair_info(info, "uInc", "info_u_inc"),
                "info_d_alt": _parse_date(_extrair_info(info, "dAlt", "info_d_alt")),
                "info_h_alt": _extrair_info(info, "hAlt", "info_h_alt"),
                "info_u_alt": _extrair_info(info, "uAlt", "info_u_alt"),
            },
        )
        total_processadas += 1

        if total_contas and (indice == total_contas or indice % 25 == 0):
            _emitir_progresso(
                progress_callback,
                etapa="contas_pagar",
                fase="gravando",
                mensagem=f"Gravando contas a pagar no banco... ({indice}/{total_contas})",
                percentual=_calcular_percentual_etapa(
                    indice_etapa,
                    0.40 + (0.60 * (indice / total_contas)),
                ),
            )

    if codigos_ativos:
        ContaPagar.objects.exclude(codigo_lancamento_omie__in=codigos_ativos).delete()

    return total_processadas


def listar_contas_receber_omie(app_key: str, app_secret: str) -> List[Dict[str, Any]]:
    contas = _listar_registros_paginados(
        url=OMIE_CONTAS_RECEBER_URL,
        call="ListarContasReceber",
        app_key=app_key,
        app_secret=app_secret,
        response_keys=["conta_receber_cadastro", "titulosEncontrados", "lista_contas_receber"],
        parametros_extras={"apenas_importado_api": "N"},
    )
    contas.sort(key=lambda item: (item.get("data_vencimento") or "", item.get("codigo_lancamento_omie") or 0))
    return contas


def importar_contas_receber_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
    indice_etapa: int = 5,
) -> int:
    _emitir_progresso(
        progress_callback,
        etapa="contas_receber",
        fase="buscando",
        mensagem="Buscando contas a receber na Omie...",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.02),
    )
    contas = listar_contas_receber_omie(app_key, app_secret)
    total_processadas = 0
    codigos_ativos = set()
    total_contas = len(contas)

    _emitir_progresso(
        progress_callback,
        etapa="contas_receber",
        fase="gravando",
        mensagem=f"Gravando contas a receber no banco... (0/{total_contas})",
        percentual=_calcular_percentual_etapa(indice_etapa, 0.40 if total_contas else 1.0),
    )

    for indice, item in enumerate(contas, start=1):
        codigo = _parse_int(_extrair_info(item, "codigo_lancamento_omie", "nCodTitulo"))
        if not codigo:
            continue

        codigos_ativos.add(codigo)
        info = item.get("info") if isinstance(item.get("info"), dict) else {}
        boleto = item.get("boleto") if isinstance(item.get("boleto"), dict) else {}

        ContaReceber.objects.update_or_create(
            codigo_lancamento_omie=codigo,
            defaults={
                "codigo_cliente_fornecedor": _parse_int(_extrair_info(item, "codigo_cliente_fornecedor", "codigo_cliente_omie")),
                "codigo_categoria": _extrair_info(item, "codigo_categoria"),
                "codigo_lancamento_integracao": _extrair_info(item, "codigo_lancamento_integracao"),
                "codigo_tipo_documento": _extrair_info(item, "codigo_tipo_documento"),
                "chave_nfe": _extrair_info(item, "chave_nfe"),
                "numero_documento_fiscal": _extrair_info(item, "numero_documento_fiscal"),
                "numero_parcela": _extrair_info(item, "numero_parcela"),
                "numero_pedido": _extrair_info(item, "numero_pedido"),
                "nCodPedido": _parse_int(_extrair_info(item, "nCodPedido")),
                "id_conta_corrente": _parse_int(_extrair_info(item, "id_conta_corrente", "nCodCC")),
                "id_origem": _extrair_info(item, "id_origem"),
                "operacao": _extrair_info(item, "operacao"),
                "tipo_agrupamento": _extrair_info(item, "tipo_agrupamento"),
                "data_emissao": _parse_date(_extrair_info(item, "data_emissao")),
                "data_previsao": _parse_date(_extrair_info(item, "data_previsao")),
                "data_registro": _parse_date(_extrair_info(item, "data_registro")),
                "data_vencimento": _parse_date(_extrair_info(item, "data_vencimento")),
                "status_titulo": _extrair_info(item, "status_titulo"),
                "valor_documento": _parse_decimal(_extrair_info(item, "valor_documento")),
                "retem_cofins": _extrair_info(item, "retem_cofins"),
                "retem_csll": _extrair_info(item, "retem_csll"),
                "retem_inss": _extrair_info(item, "retem_inss"),
                "retem_ir": _extrair_info(item, "retem_ir"),
                "retem_iss": _extrair_info(item, "retem_iss"),
                "retem_pis": _extrair_info(item, "retem_pis"),
                "boleto_cGerado": _extrair_info(boleto, "cGerado", "boleto_cGerado"),
                "boleto_cNumBancario": _extrair_info(boleto, "cNumBancario", "boleto_cNumBancario"),
                "boleto_cNumBoleto": _extrair_info(boleto, "cNumBoleto", "boleto_cNumBoleto"),
                "boleto_dDtEmBol": _parse_date(_extrair_info(boleto, "dDtEmBol", "boleto_dDtEmBol")),
                "boleto_nPerJuros": _parse_decimal(_extrair_info(boleto, "nPerJuros", "boleto_nPerJuros")),
                "boleto_nPerMulta": _parse_decimal(_extrair_info(boleto, "nPerMulta", "boleto_nPerMulta")),
                "info_cimpapi": _extrair_info(info, "cImpAPI", "info_cimpapi"),
                "info_d_inc": _parse_date(_extrair_info(info, "dInc", "info_d_inc")),
                "info_h_inc": _extrair_info(info, "hInc", "info_h_inc"),
                "info_u_inc": _extrair_info(info, "uInc", "info_u_inc"),
                "info_d_alt": _parse_date(_extrair_info(info, "dAlt", "info_d_alt")),
                "info_h_alt": _extrair_info(info, "hAlt", "info_h_alt"),
                "info_u_alt": _extrair_info(info, "uAlt", "info_u_alt"),
            },
        )
        total_processadas += 1

        if total_contas and (indice == total_contas or indice % 25 == 0):
            _emitir_progresso(
                progress_callback,
                etapa="contas_receber",
                fase="gravando",
                mensagem=f"Gravando contas a receber no banco... ({indice}/{total_contas})",
                percentual=_calcular_percentual_etapa(
                    indice_etapa,
                    0.40 + (0.60 * (indice / total_contas)),
                ),
            )

    if codigos_ativos:
        ContaReceber.objects.exclude(codigo_lancamento_omie__in=codigos_ativos).delete()

    return total_processadas


def sincronizar_dados_omie(
    app_key: str,
    app_secret: str,
    progress_callback: Callable[[Dict[str, Any]], None] | None = None,
) -> Dict[str, int]:
    return {
        "categorias": importar_categorias_omie(app_key, app_secret, progress_callback=progress_callback, indice_etapa=1),
        "clientes_fornecedores": importar_clientes_fornecedores_omie(app_key, app_secret, progress_callback=progress_callback, indice_etapa=2),
        "contas_correntes": importar_contas_correntes_omie(app_key, app_secret, progress_callback=progress_callback, indice_etapa=3),
        "contas_pagar": importar_contas_pagar_omie(app_key, app_secret, progress_callback=progress_callback, indice_etapa=4),
        "contas_receber": importar_contas_receber_omie(app_key, app_secret, progress_callback=progress_callback, indice_etapa=5),
    }
