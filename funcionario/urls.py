from django.urls import path
from funcionario.views import (
    funcionario_list,
    cargo_list,
    funcionario_manage,
    cargo_manage,
)

app_name = "funcionario"

urlpatterns = [
    path("", funcionario_list, name="list"),
    path("<int:funcionario_id>/", funcionario_manage, name="manage"),
    path("cargo/", cargo_list, name="cargo-list"),
    path("cargo/<int:cargo_id>/", cargo_manage, name="cargo-manage"),
]
