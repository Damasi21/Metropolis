from empresas.models import Empresa


def empresa_sidebar(request):
    resolver_match = getattr(request, 'resolver_match', None)
    slug = resolver_match.kwargs.get('slug') if resolver_match else None
    if not slug:
        return {}

    empresa = Empresa.objects.filter(slug__iexact=slug).only('logo').first()
    if not empresa or not empresa.logo:
        return {}

    return {'empresa_logo_url': empresa.logo.url}
