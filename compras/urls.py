from django.urls import path
from .views import compra_list, verify_nota, compra_cancelar, compra_manage

app_name = "compras"

urlpatterns = [
    path("", compra_list, name="list"),
    path("nota/", verify_nota, name="verify_nota"),
    path("cancelar/", compra_cancelar, name="cancelar"),
    path("manage/", compra_manage, name="manage"),
]
