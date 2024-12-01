from django.urls import path
from .views import (
    modelo_list,
    pagamento_list,
    pagamento_options,
    condicao_pagamento_list,
    pagamento_manage,
    condicao_pagamento_manage,
    modelo_list,
    modelo_options,
    modelo_manage,
)

app_name = "pagamento"

urlpatterns = [
    path("", pagamento_list, name="list"),
    path("options/", pagamento_options, name="options"),
    path("<int:pagamento_id>/", pagamento_manage, name="manage"),
    path("condicao/", condicao_pagamento_list, name="condicao-list"),
    path(
        "condicao/<int:condicao_pagamento_id>/",
        condicao_pagamento_manage,
        name="condicao-manage",
    ),
    path("modelo/", modelo_list, name="modelo-list"),
    path(
        "modelo/<int:modelo_id>/",
        modelo_manage,
        name="parcela-manage",
    ),
    path("modelo/options/", modelo_options, name="modelo-options"),
]
