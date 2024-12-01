from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/", include("cliente.urls")),
    path("compras/", include("compras.urls")),
    path("fornecedores/", include("fornecedor.urls")),
    path("funcionarios/", include("funcionario.urls")),
    path("local/", include("local.urls")),
    path("pagamentos/", include("pagamento.urls")),
    path("produtos/", include("produtos.urls")),
    path("vendas/", include("vendas.urls")),
    path("", include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
