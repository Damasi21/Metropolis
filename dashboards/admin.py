from django.contrib import admin

from .models import PrevistoRealizadoCategoria


@admin.register(PrevistoRealizadoCategoria)
class PrevistoRealizadoCategoriaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'categoria', 'ano', 'mes', 'projetado', 'atualizado_em')
    list_filter = ('empresa', 'ano', 'mes')
    search_fields = ('empresa__nome_empresa', 'categoria__codigo', 'categoria__descricao')
