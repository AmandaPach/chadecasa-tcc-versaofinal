from django.urls import path
from .views import (
    cidade_list,
    estado_list,
    pais_list,
    cidade_manage,
    estado_manage,
    pais_manage,
    cidade_from_estado,
)

app_name = "local"

urlpatterns = [
    path("cidades/", cidade_list, name="cidade-list"),
    path("cidades/<int:cidade_id>/", cidade_manage, name="cidade-manage"),
    path("estados/", estado_list, name="estado-list"),
    path("estados/<int:estado_id>/", estado_manage, name="estado-manage"),
    path(
        "estados/<int:estado_id>/cidades/",
        cidade_from_estado,
        name="cidade-from-estado",
    ),
    path("paises/", pais_list, name="pais-list"),
    path("paises/<int:pais_id>/", pais_manage, name="pais-manage"),
]
