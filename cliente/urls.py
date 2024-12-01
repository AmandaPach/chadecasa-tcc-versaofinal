from django.urls import path
from cliente.views import index, manage, limpar_cliente_data

app_name = "cliente"

urlpatterns = [
    path("", index, name="list"),
    path("<int:cliente_id>/", manage, name="manage"),
    path("<int:cliente_id>/limpar/", limpar_cliente_data, name="limpar"),
]
