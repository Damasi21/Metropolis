document.addEventListener('DOMContentLoaded', function () {
    // Inicializa os comportamentos da tela de parametros apos carregar o HTML.
    const formCredenciais = document.getElementById('formCredenciais');
    const btnSalvarCredenciais = document.getElementById('btnSalvarCredenciais');
    const formSincronizacaoOmie = document.getElementById('formSincronizacaoOmie');
    const blocoLoadingSincronizacao = document.getElementById('blocoLoadingSincronizacao');
    const btnSincronizarOmie = document.getElementById('btnSincronizarOmie');
    const barraProgressoSincronizacao = document.getElementById('barraProgressoSincronizacao');
    const textoStatusSincronizacao = document.getElementById('textoStatusSincronizacao');
    const campoSinal = document.getElementById('id_sinal');
    const blocoFormula = document.getElementById('bloco-formula');
    const inputPlanilhaDePara = document.getElementById('planilhaDeParaInput');
    let pollingSincronizacao = null;

    // Evita duplo envio e informa que as credenciais estao sendo salvas.
    if (formCredenciais) {
        formCredenciais.addEventListener('submit', function () {
            if (btnSalvarCredenciais) {
                btnSalvarCredenciais.disabled = true;
                btnSalvarCredenciais.innerText = 'Salvando...';
            }
        });
    }

    if (formSincronizacaoOmie) {
        // Atualiza a barra de progresso e a mensagem da sincronizacao Omie.
        const atualizarBarra = function (percentual, mensagem) {
            const percentualSeguro = Math.max(0, Math.min(100, Number(percentual) || 0));

            if (blocoLoadingSincronizacao) {
                blocoLoadingSincronizacao.classList.remove('d-none');
            }

            if (textoStatusSincronizacao && mensagem) {
                textoStatusSincronizacao.innerText = mensagem;
            }

            if (barraProgressoSincronizacao) {
                barraProgressoSincronizacao.style.width = `${percentualSeguro}%`;
                barraProgressoSincronizacao.setAttribute('aria-valuenow', String(percentualSeguro));
                barraProgressoSincronizacao.innerText = `${percentualSeguro}%`;
            }
        };

        // Interrompe a consulta periodica do status da sincronizacao.
        const encerrarPolling = function () {
            if (pollingSincronizacao) {
                window.clearInterval(pollingSincronizacao);
                pollingSincronizacao = null;
            }
        };

        // Finaliza o fluxo de sincronizacao, reabilita o botao e recarrega em caso de sucesso.
        const finalizarSincronizacao = function (mensagem, houveErro) {
            encerrarPolling();

            if (btnSincronizarOmie) {
                btnSincronizarOmie.disabled = false;
                btnSincronizarOmie.innerText = 'Atualizar cadastros e lancamentos';
            }

            if (barraProgressoSincronizacao) {
                barraProgressoSincronizacao.classList.remove('bg-danger');
                if (houveErro) {
                    barraProgressoSincronizacao.classList.add('bg-danger');
                }
            }

            atualizarBarra(100, mensagem);

            if (!houveErro) {
                window.setTimeout(function () {
                    window.location.reload();
                }, 1200);
            }
        };

        // Consulta o backend para acompanhar o andamento da tarefa Omie.
        const consultarStatus = function (taskId) {
            const template = formSincronizacaoOmie.dataset.statusUrlTemplate || '';
            const statusUrl = template.replace('__TASK_ID__', taskId);

            fetch(statusUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (resultado) {
                    const data = resultado.data;
                    if (!resultado.ok || !data.ok) {
                        throw new Error(data.mensagem || 'Nao foi possivel consultar o andamento da sincronizacao.');
                    }

                    atualizarBarra(data.percentual, data.mensagem);

                    if (data.state === 'completed') {
                        finalizarSincronizacao(data.mensagem, false);
                    } else if (data.state === 'error') {
                        finalizarSincronizacao(data.mensagem, true);
                    }
                })
                .catch(function (error) {
                    finalizarSincronizacao(error.message || 'Erro ao acompanhar a sincronizacao.', true);
                });
        };

        // Inicia a sincronizacao Omie via AJAX e passa a acompanhar o status por polling.
        formSincronizacaoOmie.addEventListener('submit', function (event) {
            event.preventDefault();

            if (blocoLoadingSincronizacao) {
                blocoLoadingSincronizacao.classList.remove('d-none');
            }

            if (btnSincronizarOmie) {
                btnSincronizarOmie.disabled = true;
                btnSincronizarOmie.innerText = 'Sincronizando...';
            }

            atualizarBarra(2, 'Preparando sincronizacao com a Omie...');

            const startUrl = formSincronizacaoOmie.dataset.startUrl;
            const csrfTokenInput = formSincronizacaoOmie.querySelector('input[name="csrfmiddlewaretoken"]');
            const csrfToken = csrfTokenInput ? csrfTokenInput.value : '';

            fetch(startUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ acao: 'sincronizar_omie' }),
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (resultado) {
                    const data = resultado.data;
                    if (!resultado.ok || !data.ok) {
                        throw new Error(data.mensagem || 'Nao foi possivel iniciar a sincronizacao.');
                    }

                    consultarStatus(data.task_id);
                    pollingSincronizacao = window.setInterval(function () {
                        consultarStatus(data.task_id);
                    }, 1500);
                })
                .catch(function (error) {
                    finalizarSincronizacao(error.message || 'Erro ao iniciar a sincronizacao.', true);
                });
        });
    }

    // Mostra o campo de formula somente quando o sinal selecionado for "resultado".
    function alternarFormula() {
        if (!campoSinal || !blocoFormula) {
            return;
        }

        blocoFormula.style.display = campoSinal.value === 'resultado' ? 'block' : 'none';
    }

    if (campoSinal) {
        campoSinal.addEventListener('change', alternarFormula);
        alternarFormula();
    }

    // Aciona inputs de upload escondidos a partir de botoes visiveis.
    document.querySelectorAll('[data-planilha-trigger]').forEach(function (botao) {
        botao.addEventListener('click', function () {
            const targetId = botao.dataset.planilhaTrigger;
            const input = targetId ? document.getElementById(targetId) : null;
            if (input) {
                input.click();
            }
        });
    });

    // Envia automaticamente a planilha De/Para assim que um arquivo for escolhido.
    if (inputPlanilhaDePara) {
        inputPlanilhaDePara.addEventListener('change', function () {
            if (inputPlanilhaDePara.files.length && inputPlanilhaDePara.form) {
                inputPlanilhaDePara.form.submit();
            }
        });
    }

    document.querySelectorAll('[data-planilha-auto-submit]').forEach(function (input) {
        input.addEventListener('change', function () {
            if (input.files.length && input.form) {
                input.form.submit();
            }
        });
    });
});
