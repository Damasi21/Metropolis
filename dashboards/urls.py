from django.urls import path
from .views import (
    mover_conta_dre,
    dashboard_empresa,
    parametros_empresa,
    dashboard_resultado,
    contas_dre,
    depara_categoria_dre,
    excluir_conta_dre,
    indicadores,
    exportar_planilha_depara,
    iniciar_sincronizacao_omie,
    status_sincronizacao_omie,
)


urlpatterns = [
    path('<slug:slug>/', dashboard_empresa, name='dashboard_empresa'),
    path('<slug:slug>/resultado/', dashboard_resultado, name='dashboard_resultado'),
    path('<slug:slug>/parametros/', parametros_empresa, name='parametros_empresa'),
    path('<slug:slug>/parametros/sincronizacao-omie/iniciar/', iniciar_sincronizacao_omie, name='iniciar_sincronizacao_omie'),
    path('<slug:slug>/parametros/sincronizacao-omie/status/<str:task_id>/', status_sincronizacao_omie, name='status_sincronizacao_omie'),
    path('<slug:slug>/parametros/contas-dre/', contas_dre, name='contas_dre'),
    path('<slug:slug>/parametros/indicadores/', indicadores, name='indicadores'),
    path('<slug:slug>/parametros/contas-dre/excluir/<int:id>/', excluir_conta_dre, name='excluir_conta_dre'),
    path('<slug:slug>/parametros/de-para/', depara_categoria_dre, name='depara_categoria_dre'),
    path('<slug:slug>/parametros/de-para/exportar/', exportar_planilha_depara, name='exportar_planilha_depara'),
    path('<slug:slug>/parametros/contas-dre/mover/<int:id>/<str:direcao>/', mover_conta_dre, name='mover_conta_dre'),
]
