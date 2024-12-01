from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import Cliente
from local.models import Cidade, Estado, Pais
from vendas.models import Vendas
from utils import process_form_data, validar_cpf

@csrf_exempt
def limpar_cliente_data(request, cliente_id):
    if request.method != "GET":
        return HttpResponse(status=405, content="Método não permitido")

    Cliente.get(cliente_id)

    cleared_data = {
        "nome_cliente": "***",
        "sobrenome_cliente": "***",
        "telefone_cliente": "***",
        "data_nascimento_cliente": "***",
        "cpf_cliente": "***",
        "rg_cliente": "***",
        "rua_cliente": "***",
        "cep_cliente": "***",
        "bairro_cliente": "***",
        "numero_rua_cliente": "***",
        "complemento_cliente": "***",
        "cidade_id" : "-1",
        "estado_id": "-1",
        "apagado": True,
        "data_cadastro": "***",
    }
    Cliente.update(cliente_id, **cleared_data)
    return HttpResponse(status=200)

def index(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        cliente_id = str(data.pop("id", ""))
        data["status"] = data.get("status", "") == "on"

        cidade_id = data.get("cidade_id")
        cidade = Cidade.get(cidade_id)
        pais = Cidade.query(f"SELECT Pais.* FROM Pais, Estado, Cidade WHERE Pais.id = Estado.pais_id AND Estado.id = {cidade['estado_id']}")[0]
        estrangeiro = pais['atual'] == 'False'
        data["estrangeiro_cliente"] = estrangeiro
        data["apagado"] = False

        required_fields = [
            "nome_cliente",
            "sobrenome_cliente",
            "sexo_cliente",
            "data_nascimento_cliente",
            "rua_cliente",
            "numero_rua_cliente",
            "telefone_cliente",
            "bairro_cliente",
            "cep_cliente",
            "cidade_id",
        ]
        for field in required_fields:
            if not data.get(field):
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)
        cpf_cliente = data.get("cpf_cliente")
        if not estrangeiro and not validar_cpf(cpf_cliente):
            return HttpResponse("CPF inválido. Verifique e tente novamente", status=400)

        unique_fields = {
            "cpf_cliente": ("CPF", cpf_cliente),
            "rg_cliente": ("RG", data.get("rg_cliente")),
        }

        for field, (field_name, field_value) in unique_fields.items():
            if not field_value:
                if estrangeiro:
                    continue
                return HttpResponse(
                    f"{field_name} é obrigatório para nativos", status=400
                )

            unique_lista = Cliente.list(
                **{
                    field: (
                        field_value
                        if not isinstance(field_value, list)
                        else field_value[0]
                    )
                }
            )
            if (
                unique_lista
                and "id" not in data
                and str(unique_lista[0]["id"]) != cliente_id
            ):
                return HttpResponse(
                    f'{field_name} "{field_value}" já cadastrado', status=400
                )

        if cliente_id:
            vendas = Vendas.list(cliente_id=cliente_id, cancelado=0)
            vendas += Vendas.list(cliente_id=cliente_id, cancelado=False)
            if vendas:
                return HttpResponse(
                    "Cliente possui vendas associadas e não pode ser alterado",
                    status=400,
                )
            Cliente.update(cliente_id, **data)
            return HttpResponse(status=200)

        Cliente.create(data)
        new_cliente = Cliente.list()[-1]
        new_cliente["nome"] = new_cliente.get("nome_cliente")
        return JsonResponse(new_cliente, status=200)

    clientes = Cliente.list()
    cidades = Cidade.list()
    estados = Estado.list()
    paises = Pais.list()

    return render(
        request,
        "cliente/cliente_list.html",
        {
            "clientes": clientes,
            "cidades": cidades,
            "estados": estados,
            "paises": paises,
        },
    )


@csrf_exempt
def manage(request, cliente_id):
    if request.method == "DELETE":
        vendas = Vendas.list(cliente_id=cliente_id, cancelado=0)
        vendas += Vendas.list(cliente_id=cliente_id, cancelado=False)
        if vendas:
            return HttpResponse(
                "Cliente possui vendas associadas e não pode ser removido.",
                status=400,
            )
        Cliente.delete_from_id(cliente_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        cliente = Cliente.get(cliente_id)
        if not cliente:
            return HttpResponse(status=400, content="Cliente não encontrado")
        cliente["nome"] = Cidade.get("nome_cliente")
        cliente_cidade_id = cliente.get("cidade_id")
        cliente_estado_id = cliente.get("estado_id")
        cliente_cidade = Cidade.get(cliente_cidade_id) if cliente_cidade_id else None
        cliente_estado = Estado.get(cliente_estado_id) if cliente_estado_id else None
        cliente["cidade_nome"] = cliente_cidade
        cliente["estado_nome"] = cliente_estado
        return JsonResponse(cliente, status=200)

    return HttpResponse(status=400, content="Método não permitido")
