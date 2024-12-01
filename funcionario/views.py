from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Funcionario, Cargo
from local.models import Cidade, Estado, Pais
from utils import process_form_data, validar_cpf

funcionario_required_fields = [
    "nome_funcionario",
    "sobrenome_funcionario",
    "sexo_funcionario",
    "telefone_funcionario",
    "data_nascimento_funcionario",
    "rua_funcionario",
    "numero_rua_funcionario",
    "cep_funcionario",
    "cidade_id",
    "cargo_id",
]

cargo_required_fields = ["nome_cargo"]


def funcionario_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        funcionario_id = str(data.pop("id", ""))
        funcionario_cpf = data.get("cpf_funcionario")

        if funcionario_cpf and not validar_cpf(funcionario_cpf):
            return HttpResponse("CPF inválido. Verifique e tente novamente", status=400)

        for field in funcionario_required_fields:
            if not data.get(field):
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)

        unique_fields = {
            "cpf_funcionario": ("CPF", data.get("cpf_funcionario")),
            "rg_funcionario": ("RG", data.get("rg_funcionario")),
        }

        cidade_id = data.get("cidade_id")
        cidade = Cidade.get(cidade_id)
        pais = Cidade.query(f"SELECT Pais.* FROM Pais, Estado, Cidade WHERE Pais.id = Estado.pais_id AND Estado.id = {cidade['estado_id']}")[0]
        estrangeiro = pais['atual'] == 'False'
        data["estrangeiro_funcionario"] = bool(estrangeiro)

        if not estrangeiro:
            for field, (field_name, field_value) in unique_fields.items():
                if not field_value:
                    return HttpResponse(f"{field_name} não informado", status=400)

                unique_lista = Funcionario.list(**{field: field_value})
                if unique_lista and (
                    funcionario_id or str(unique_lista[0]["id"]) != funcionario_id
                ):
                    return HttpResponse(
                        f'{field_name} "{field_value}" já cadastrado', status=400
                    )

        if funcionario_id:
            Funcionario.update(funcionario_id, **data)
            return HttpResponse(status=200)

        Funcionario.create(data)
        novo_funcionario = Funcionario.list()[-1]
        novo_funcionario["nome"] = novo_funcionario.get("nome_funcionario")
        return JsonResponse(novo_funcionario, status=200)

    funcionarios = Funcionario.list()
    for funcionario in funcionarios:
        funcionario_cargo = Cargo.get(funcionario["cargo_id"])
        funcionario_cidade = Cidade.get(funcionario["cidade_id"])
        if funcionario_cargo:
            funcionario["cargo_nome"] = funcionario_cargo["nome_cargo"]
        if funcionario_cidade:
            funcionario["cidade"] = funcionario_cidade["nome_cidade"]
    cargos = Cargo.list()
    cidades = Cidade.list()
    estados = Estado.list()
    paises = Pais.list()
    return render(
        request,
        "funcionario/funcionario_list.html",
        {
            "funcionarios": funcionarios,
            "cargos": cargos,
            "cidades": cidades,
            "estados": estados,
            "paises": paises,
        },
    )


@csrf_exempt
def funcionario_manage(request, funcionario_id):
    if request.method == "DELETE":
        Funcionario.delete_from_id(funcionario_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        funcionario = Funcionario.get(funcionario_id)
        if not funcionario:
            return HttpResponse(status=400, content="Funcionário não encontrado")
        funcionario["nome"] = funcionario.get("nome_funcionario")
        return JsonResponse(funcionario, status=200)

    return HttpResponse(status=400, content="Método não permitido")


def cargo_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        cargo_id = str(data.pop("id", ""))

        for field in cargo_required_fields:
            if not data.get(field):
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)

        cargos_existentes = Cargo.list(nome_cargo=data["nome_cargo"])
        if cargos_existentes and (
            not cargo_id or str(cargos_existentes[0]["id"]) != cargo_id
        ):
            return HttpResponse(
                status=400, content="Já existe um Cargo com esse nome cadastrado."
            )

        if cargo_id:
            Cargo.update(cargo_id, **data)
            return HttpResponse(status=200)

        Cargo.create(data)
        novo_cargo = Cargo.list()[-1]
        novo_cargo["nome"] = novo_cargo.get("nome_cargo")
        return JsonResponse(novo_cargo, status=200)
    cargos = Cargo.list()
    return render(request, "funcionario/cargo_list.html", {"cargos": cargos})


@csrf_exempt
def cargo_manage(request, cargo_id):
    if request.method == "DELETE":
        funcionarios = Funcionario.list(cargo_id=cargo_id)
        if funcionarios:
            return HttpResponse(
                status=400,
                content=f"Não é possível remover um Cargo que possui funcionários. Remova os funcionários primeiro: {', '.join([funcionario['nome_funcionario'] for funcionario in funcionarios])}",
            )
        Cargo.delete_from_id(cargo_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        cargo = Cargo.get(cargo_id)
        if not cargo:
            return HttpResponse(status=400, content="Cargo não encontrado")
        cargo["nome"] = cargo.get("nome_cargo")
        return JsonResponse(cargo, status=200)

    return HttpResponse(status=400, content="Método não permitido")
