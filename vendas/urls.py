from django.urls import path
from .views import venda_list, verify_nota, venda_manage, venda_cancelar

app_name = "vendas"

urlpatterns = [
    path("", venda_list, name="list"),
    path("manage/", venda_manage, name="manage"),
    path("nota", verify_nota, name="verify_nota"),
    path("cancelar/", venda_cancelar, name="cancelar"),
]