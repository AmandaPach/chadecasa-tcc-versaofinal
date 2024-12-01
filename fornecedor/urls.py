from django.urls import path
from fornecedor.views import fornecedor_list, manage

app_name = "fornecedor"

urlpatterns = [
    path("", fornecedor_list, name="list"),
    path("<int:fornecedor_id>/", manage, name="manage"),
]
