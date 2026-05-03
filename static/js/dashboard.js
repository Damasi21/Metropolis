document.addEventListener('DOMContentLoaded', function () {
    // Inicializa os comportamentos globais do dashboard quando a tela termina de carregar.
    inicializarMenuLateral();
    inicializarModalExclusao();
    inicializarModalMensagem();
    inicializarFiltroPeriodo();
    inicializarDashboardResultado();
    inicializarDashboardVisaoGeral();
});

// Controla o estado visual dos botoes do menu lateral.
function inicializarMenuLateral() {
    const botoes = document.querySelectorAll('.menu-btn');

    botoes.forEach(function (btn) {
        btn.addEventListener('click', function () {
            botoes.forEach(function (botao) {
                botao.classList.remove('active');
            });

            btn.classList.add('active');
        });
    });
}

// Prepara o modal de exclusao e ajusta a URL do formulario conforme o item selecionado.
function inicializarModalExclusao() {
    const modal = document.getElementById('modalExcluir');
    const form = document.getElementById('formExcluir');

    if (!modal || !form) {
        return;
    }

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        if (!button) {
            return;
        }

        const id = button.getAttribute('data-id');
        const slug = window.location.pathname.split('/')[2];
        form.action = `/dashboard/${slug}/parametros/contas-dre/excluir/${id}/`;
    });
}

// Abre automaticamente o modal de mensagem quando o backend sinaliza essa necessidade.
function inicializarModalMensagem() {
    const modalMensagem = document.getElementById('modalMensagem');

    if (!modalMensagem || modalMensagem.dataset.autoOpen !== 'true') {
        return;
    }

    const modal = new bootstrap.Modal(modalMensagem);
    modal.show();
}

function inicializarFiltroPeriodo() {
    const trees = document.querySelectorAll('[data-periodo-tree]');

    trees.forEach(function (tree) {
        const form = tree.closest('form');
        const input = form ? form.querySelector('[data-periodo-input]') : null;
        const trigger = tree.querySelector('[data-periodo-trigger]');
        const menu = tree.querySelector('[data-periodo-menu]');
        const options = Array.from(tree.querySelectorAll('[data-periodo-value]'));

        if (!form || !input || !trigger || !menu || !options.length) {
            return;
        }

        function fecharMenu() {
            tree.classList.remove('periodo-tree-open');
            trigger.setAttribute('aria-expanded', 'false');
        }

        function abrirMenu() {
            tree.classList.add('periodo-tree-open');
            trigger.setAttribute('aria-expanded', 'true');
        }

        function alternarGrupo(nivel, ano, trimestre) {
            const selector = nivel === 'ano'
                ? `[data-periodo-nivel="trimestre"][data-periodo-ano="${ano}"]`
                : `[data-periodo-nivel="mes"][data-periodo-ano="${ano}"][data-periodo-trimestre="${trimestre}"]`;
            const filhos = Array.from(tree.querySelectorAll(selector));
            const abrir = filhos.some(function (filho) {
                return !filho.classList.contains('periodo-tree-visible');
            });

            filhos.forEach(function (filho) {
                filho.classList.toggle('periodo-tree-visible', abrir);

                if (!abrir && nivel === 'ano' && filho.dataset.periodoNivel === 'trimestre') {
                    const meses = tree.querySelectorAll(
                        `[data-periodo-nivel="mes"][data-periodo-ano="${ano}"][data-periodo-trimestre="${filho.dataset.periodoTrimestre}"]`
                    );
                    meses.forEach(function (mes) {
                        mes.classList.remove('periodo-tree-visible');
                    });
                    const icon = filho.querySelector('.periodo-tree-icon');
                    if (icon) {
                        icon.textContent = '+';
                    }
                }
            });
        }

        function selecionarPeriodo(option) {
            input.value = option.dataset.periodoValue;
            trigger.textContent = option.dataset.periodoValue === 'customizado'
                ? 'Selecionar periodo'
                : option.dataset.periodoLabel;

            options.forEach(function (item) {
                item.classList.remove('active');
            });
            option.classList.add('active');
            fecharMenu();
            form.submit();
        }

        trigger.addEventListener('click', function () {
            if (tree.classList.contains('periodo-tree-open')) {
                fecharMenu();
                return;
            }

            abrirMenu();
        });

        options.forEach(function (option) {
            const nivel = option.dataset.periodoNivel;

            if (option.classList.contains('active')) {
                if (nivel === 'trimestre' || nivel === 'mes') {
                    tree.querySelectorAll(`[data-periodo-nivel="trimestre"][data-periodo-ano="${option.dataset.periodoAno}"]`).forEach(function (trimestre) {
                        trimestre.classList.add('periodo-tree-visible');
                    });
                }

                if (nivel === 'mes') {
                    tree.querySelectorAll(`[data-periodo-nivel="mes"][data-periodo-ano="${option.dataset.periodoAno}"][data-periodo-trimestre="${option.dataset.periodoTrimestre}"]`).forEach(function (mes) {
                        mes.classList.add('periodo-tree-visible');
                    });
                }
            }

            option.addEventListener('click', function (event) {
                if (nivel === 'ano' || nivel === 'trimestre') {
                    const icon = option.querySelector('.periodo-tree-icon');

                    if (event.target.closest('.periodo-tree-icon')) {
                        alternarGrupo(nivel, option.dataset.periodoAno, option.dataset.periodoTrimestre);
                        if (icon) {
                            icon.textContent = icon.textContent === '+' ? '-' : '+';
                        }
                        return;
                    }
                }

                selecionarPeriodo(option);
            });
        });

        document.addEventListener('click', function (event) {
            if (!tree.contains(event.target)) {
                fecharMenu();
            }
        });
    });
}

// Agrupa as interacoes da tela de resultado do DRE: scroll, colapso, linhas e grafico.
function inicializarDashboardResultado() {
    const topScroll = document.getElementById('dreScrollTop');
    const topInner = document.getElementById('dreScrollTopInner');
    const tableWrapper = document.getElementById('dreTableWrapper');
    const dreCollapse = document.getElementById('painelDreTabela');
    const dreToggleBtn = document.querySelector('.dre-toggle-btn');
    const dreExpandAllBtn = document.getElementById('dreExpandAllBtn');
    const dreCollapseAllBtn = document.getElementById('dreCollapseAllBtn');
    const dreContaPaiSelect = document.getElementById('dreContaPaiSelect');
    const dreGraficoMediaMensal = document.getElementById('dreGraficoMediaMensal');
    const dreGraficoPlot = document.getElementById('dreGraficoPlot');
    const variacaoMensalTitulo = document.getElementById('variacaoMensalTitulo');
    const variacaoMensalPlot = document.getElementById('variacaoMensalPlot');
    const variacaoMensalAno = document.getElementById('variacaoMensalAno');
    const dreContasPaiDataNode = document.getElementById('dre-contas-pai-data');
    const dreContasPaiData = dreContasPaiDataNode ? JSON.parse(dreContasPaiDataNode.textContent) : [];

    if (!topScroll || !topInner || !tableWrapper) {
        return;
    }

    // Mantem a barra de rolagem superior com a mesma largura da tabela DRE.
    function syncTopWidth() {
        const table = tableWrapper.querySelector('table');
        if (!table) {
            return;
        }
        topInner.style.width = `${table.scrollWidth}px`;
    }

    let syncingTop = false;
    let syncingBottom = false;

    topScroll.addEventListener('scroll', function () {
        if (syncingBottom) {
            syncingBottom = false;
            return;
        }
        syncingTop = true;
        tableWrapper.scrollLeft = topScroll.scrollLeft;
    });

    tableWrapper.addEventListener('scroll', function () {
        if (syncingTop) {
            syncingTop = false;
            return;
        }
        syncingBottom = true;
        topScroll.scrollLeft = tableWrapper.scrollLeft;
    });

    syncTopWidth();
    window.addEventListener('resize', syncTopWidth);

    if (dreCollapse && dreToggleBtn) {
        dreCollapse.addEventListener('shown.bs.collapse', function () {
            const icone = dreToggleBtn.querySelector('.fs-6');
            const spans = dreToggleBtn.querySelectorAll('span');

            if (icone) {
                icone.textContent = 'v';
            }

            if (spans.length) {
                spans[0].textContent = 'Encolher tabela do DRE';
            }

            syncTopWidth();
        });

        dreCollapse.addEventListener('hidden.bs.collapse', function () {
            const icone = dreToggleBtn.querySelector('.fs-6');
            const spans = dreToggleBtn.querySelectorAll('span');

            if (icone) {
                icone.textContent = '>';
            }

            if (spans.length) {
                spans[0].textContent = 'Expandir tabela do DRE';
            }
        });
    }

    const childLookup = new Map();

    tableWrapper.querySelectorAll('tbody tr[data-row-id]').forEach(function (row) {
        const rowId = row.dataset.rowId;
        const parentId = row.dataset.parentId;

        if (!parentId) {
            return;
        }

        if (!childLookup.has(parentId)) {
            childLookup.set(parentId, []);
        }

        childLookup.get(parentId).push(row);
    });

    // Esconde todos os filhos de uma linha, incluindo niveis mais profundos da hierarquia.
    function hideDescendants(rowId) {
        const children = childLookup.get(rowId) || [];
        children.forEach(function (child) {
            child.style.display = 'none';
            hideDescendants(child.dataset.rowId);

            const toggle = child.querySelector('.dre-row-toggle[data-target-id]');
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
                const icon = toggle.querySelector('.dre-row-toggle-icon');
                if (icon) {
                    icon.textContent = '+';
                }
            }
        });
    }

    // Exibe apenas os filhos diretos de uma linha da tabela DRE.
    function showChildren(rowId) {
        const children = childLookup.get(rowId) || [];
        children.forEach(function (child) {
            child.style.display = '';
        });
    }

    // Atualiza o atributo de acessibilidade e o icone de abrir/fechar da linha.
    function setToggleState(row, expanded) {
        const toggle = row.querySelector('.dre-row-toggle[data-target-id]');
        if (!toggle) {
            return;
        }

        toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        const icon = toggle.querySelector('.dre-row-toggle-icon');
        if (icon) {
            icon.textContent = expanded ? '-' : '+';
        }
    }

    // Abre todos os niveis da tabela DRE.
    function expandAllRows() {
        tableWrapper.querySelectorAll('tbody tr[data-row-id]').forEach(function (row) {
            row.style.display = '';
            setToggleState(row, true);
        });
    }

    // Fecha a tabela deixando visiveis somente as contas pai.
    function collapseToParents() {
        tableWrapper.querySelectorAll('tbody tr[data-row-id]').forEach(function (row) {
            row.style.display = row.dataset.parentId ? 'none' : '';
            setToggleState(row, false);
        });
    }

    tableWrapper.querySelectorAll('.dre-row-toggle[data-target-id]').forEach(function (button) {
        button.addEventListener('click', function () {
            const targetId = button.dataset.targetId;
            const expanded = button.getAttribute('aria-expanded') === 'true';
            const icon = button.querySelector('.dre-row-toggle-icon');

            if (expanded) {
                hideDescendants(targetId);
                button.setAttribute('aria-expanded', 'false');
                if (icon) {
                    icon.textContent = '+';
                }
                return;
            }

            showChildren(targetId);
            button.setAttribute('aria-expanded', 'true');
            if (icon) {
                icon.textContent = '-';
            }
        });
    });

    if (dreExpandAllBtn) {
        dreExpandAllBtn.addEventListener('click', expandAllRows);
    }

    if (dreCollapseAllBtn) {
        dreCollapseAllBtn.addEventListener('click', collapseToParents);
    }

    // Evita que textos muito proximos disputem o mesmo espaco visual no grafico.
    function ocultarValoresSobrepostos() {
        const valores = Array.from(dreGraficoPlot.querySelectorAll('.dre-grafico-coluna-valor'));
        let limiteDireito = -Infinity;

        valores.forEach(function (valor) {
            valor.classList.remove('dre-grafico-coluna-valor-oculto');

            const retangulo = valor.getBoundingClientRect();
            if (retangulo.left < limiteDireito + 4) {
                valor.classList.add('dre-grafico-coluna-valor-oculto');
                return;
            }

            limiteDireito = retangulo.right;
        });
    }

    function escapeHtml(valor) {
        return String(valor || '').replace(/[&<>"']/g, function (caractere) {
            return {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#39;',
            }[caractere];
        });
    }

    function renderizarGraficoVariacaoMensal(contaSelecionada) {
        if (!variacaoMensalPlot) {
            return;
        }

        const variacao = contaSelecionada ? contaSelecionada.variacao_mensal : null;
        const colunas = variacao && Array.isArray(variacao.colunas) ? variacao.colunas : [];
        const nomeConta = contaSelecionada ? contaSelecionada.nome : '';

        if (variacaoMensalTitulo && variacao) {
            variacaoMensalTitulo.textContent = variacao.titulo || 'Variacao mensal';
        }

        if (variacaoMensalAno) {
            variacaoMensalAno.textContent = variacao && variacao.ano ? variacao.ano : '';
        }

        if (!colunas.length) {
            variacaoMensalPlot.className = 'dre-grafico-vazio text-muted';
            variacaoMensalPlot.removeAttribute('style');
            variacaoMensalPlot.setAttribute('aria-label', `Variacao mensal da ${nomeConta}`);
            variacaoMensalPlot.textContent = `Nenhum dado de AH encontrado para ${nomeConta || 'a conta selecionada'}.`;
            return;
        }

        const colunasHtml = colunas.map(function (coluna) {
            const percentual = escapeHtml(coluna.percentual);
            const rotulo = escapeHtml(coluna.rotulo);
            const altura = escapeHtml(coluna.altura);

            if (coluna.direcao === 'alta') {
                return `
                    <div class="variacao-mensal-coluna">
                        <div class="variacao-mensal-metade variacao-mensal-metade-superior">
                            <span class="variacao-mensal-valor">${percentual}</span>
                            <span class="variacao-mensal-seta variacao-mensal-seta-alta"></span>
                            <span class="variacao-mensal-barra variacao-mensal-barra-positiva" style="height: ${altura}%;"></span>
                        </div>
                        <div class="variacao-mensal-metade variacao-mensal-metade-inferior"></div>
                        <span class="variacao-mensal-rotulo">${rotulo}</span>
                    </div>
                `;
            }

            if (coluna.direcao === 'baixa') {
                return `
                    <div class="variacao-mensal-coluna">
                        <div class="variacao-mensal-metade variacao-mensal-metade-superior"></div>
                        <div class="variacao-mensal-metade variacao-mensal-metade-inferior">
                            <span class="variacao-mensal-barra variacao-mensal-barra-negativa" style="height: ${altura}%;"></span>
                            <span class="variacao-mensal-valor">${percentual}</span>
                            <span class="variacao-mensal-seta variacao-mensal-seta-baixa"></span>
                        </div>
                        <span class="variacao-mensal-rotulo">${rotulo}</span>
                    </div>
                `;
            }

            return `
                <div class="variacao-mensal-coluna">
                    <div class="variacao-mensal-metade variacao-mensal-metade-superior"></div>
                    <div class="variacao-mensal-metade variacao-mensal-metade-inferior"></div>
                    <span class="variacao-mensal-rotulo">${rotulo}</span>
                </div>
            `;
        }).join('');

        variacaoMensalPlot.className = 'variacao-mensal-plot';
        variacaoMensalPlot.style.setProperty('--variacao-colunas', colunas.length);
        variacaoMensalPlot.setAttribute('aria-label', `Variacao mensal da ${nomeConta}`);
        variacaoMensalPlot.innerHTML = `<div class="variacao-mensal-eixo"></div>${colunasHtml}`;
    }

    // Renderiza o grafico mensal e a media da conta pai selecionada.
    function renderizarGraficoContaPai(contaId) {
        if (!dreGraficoPlot || !dreGraficoMediaMensal) {
            return;
        }

        const contaSelecionada = dreContasPaiData.find(function (item) {
            return String(item.id) === String(contaId);
        });

        if (!contaSelecionada || !contaSelecionada.colunas.length) {
            dreGraficoMediaMensal.textContent = '-';
            dreGraficoPlot.innerHTML = '<div class="dre-grafico-vazio text-muted">Nenhum dado disponível para o período selecionado.</div>';
            renderizarGraficoVariacaoMensal(contaSelecionada);
            return;
        }

        dreGraficoMediaMensal.textContent = contaSelecionada.media_mensal;
        renderizarGraficoVariacaoMensal(contaSelecionada);

        const maximo = Math.max.apply(null, contaSelecionada.colunas.map(function (coluna) {
            return Math.abs(coluna.valor);
        }).concat([1]));

        const colunasHtml = contaSelecionada.colunas.map(function (coluna) {
            const altura = Math.max((Math.abs(coluna.valor) / maximo) * 100, 4);
            const classeBarra = coluna.valor < 0 ? 'negativa' : '';
            return `
                <div class="dre-grafico-coluna">
                    <div class="dre-grafico-coluna-corpo" style="--altura-coluna: ${altura}%">
                        <div class="dre-grafico-coluna-valor ${classeBarra}">${coluna.valor_formatado}</div>
                        <div class="dre-grafico-barra ${classeBarra}" style="height: ${altura}%"></div>
                    </div>
                    <div class="dre-grafico-coluna-rotulo">${coluna.rotulo}</div>
                </div>
            `;
        }).join('');

        dreGraficoPlot.innerHTML = `<div class="dre-grafico-colunas">${colunasHtml}</div>`;
        window.requestAnimationFrame(ocultarValoresSobrepostos);
    }

    if (dreContaPaiSelect) {
        dreContaPaiSelect.addEventListener('change', function () {
            renderizarGraficoContaPai(dreContaPaiSelect.value);
        });

        if (dreContasPaiData.length) {
            dreContaPaiSelect.value = String(dreContasPaiData[0].id);
            renderizarGraficoContaPai(dreContaPaiSelect.value);
        }
    }
}

function inicializarDashboardVisaoGeral() {
    const graficoTempo = document.getElementById('visaoGraficoTempo');
    const graficoMargem = document.getElementById('visaoGraficoMargem');

    if (!graficoTempo && !graficoMargem) {
        return;
    }

    function lerJson(id) {
        const node = document.getElementById(id);
        return node ? JSON.parse(node.textContent) : [];
    }

    function escapeHtml(valor) {
        return String(valor || '').replace(/[&<>"']/g, function (caractere) {
            return {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#39;',
            }[caractere];
        });
    }

    function alturaCss(valor) {
        return `${Number(valor || 0).toFixed(2)}%`;
    }

    function renderizarGraficoTempo() {
        if (!graficoTempo) {
            return;
        }

        const dados = lerJson('visao-grafico-tempo-data');
        if (!dados.length) {
            graficoTempo.className = 'dre-grafico-vazio text-muted';
            graficoTempo.textContent = 'Nenhum dado encontrado para o periodo selecionado.';
            return;
        }

        const colunasHtml = dados.map(function (item) {
            const alturaRecebimentos = alturaCss(item.altura_recebimentos);
            const alturaPagamentos = alturaCss(item.altura_pagamentos);
            const rotulo = escapeHtml(item.rotulo);
            const ano = escapeHtml(item.ano);

            return `
                <div class="visao-grafico-grupo">
                    <div class="visao-grafico-barra-wrap" style="--altura-barra: ${alturaRecebimentos}">
                        <span class="visao-grafico-valor">${escapeHtml(item.recebimentos_formatado)}</span>
                        <span class="visao-grafico-barra" style="height: ${alturaRecebimentos}"></span>
                    </div>
                    <div class="visao-grafico-barra-wrap" style="--altura-barra: ${alturaPagamentos}">
                        <span class="visao-grafico-valor">${escapeHtml(item.pagamentos_formatado)}</span>
                        <span class="visao-grafico-barra visao-grafico-barra-pagamentos" style="height: ${alturaPagamentos}"></span>
                    </div>
                    <div class="visao-grafico-rotulo">${rotulo}<span class="visao-grafico-ano">${ano}</span></div>
                </div>
            `;
        }).join('');

        graficoTempo.innerHTML = `<div class="visao-grafico-scroll-track">${colunasHtml}</div>`;
        ajustarLarguraMesesGraficoTempo();
    }

    function ajustarLarguraMesesGraficoTempo() {
        if (!graficoTempo) {
            return;
        }

        const larguraUtil = graficoTempo.clientWidth - 24;
        const larguraGaps = 28 * 5;
        const larguraMes = Math.max((larguraUtil - larguraGaps) / 6, 92);
        graficoTempo.style.setProperty('--visao-mes-largura', `${larguraMes.toFixed(2)}px`);
    }

    function renderizarGraficoMargem() {
        if (!graficoMargem) {
            return;
        }

        const dados = lerJson('visao-grafico-margem-data');
        if (!dados.length) {
            graficoMargem.className = 'dre-grafico-vazio text-muted';
            graficoMargem.textContent = 'Nenhum dado encontrado para o periodo selecionado.';
            return;
        }

        graficoMargem.innerHTML = dados.map(function (item) {
            const altura = alturaCss(item.altura);
            const rotulo = escapeHtml(item.rotulo);
            const ano = escapeHtml(item.ano);

            return `
                <div class="visao-grafico-grupo">
                    <div class="visao-grafico-barra-wrap" style="--altura-barra: ${altura}">
                        <span class="visao-grafico-valor">${escapeHtml(item.percentual)}</span>
                        <span class="visao-grafico-barra" style="height: ${altura}"></span>
                    </div>
                    <div class="visao-grafico-rotulo">${rotulo}<span class="visao-grafico-ano">${ano}</span></div>
                </div>
            `;
        }).join('');
    }

    renderizarGraficoTempo();
    renderizarGraficoMargem();

    window.addEventListener('resize', ajustarLarguraMesesGraficoTempo);
}
