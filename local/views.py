from os import name
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pais, Estado, Cidade
from cliente.models import Cliente
from utils import process_form_data


def pais_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        pais_id = str(data.pop("id", ""))
        if not data.get("nome_pais", False):
            return HttpResponse(status=400, content="Campos não preenchidos")

        pais_existente = Pais.list(nome_pais=data["nome_pais"])
        pais_atual = data.get("atual", "").lower() == "on"
        data["atual"] = pais_atual

        if pais_id:
            Pais.update(pais_id, **data)
            return HttpResponse(status=200)

        if pais_existente and (pais_existente[0]["id"] != pais_id or not pais_id):
            return HttpResponse(
                status=400, content="Já existe um País com esse nome cadastrado."
            )

        Pais.create(data)
        novo_pais = Pais.list()[-1]
        novo_pais['nome'] = novo_pais.get('nome_pais')
        return JsonResponse(novo_pais, status=200)

    paises = Pais.list()
    return render(request, "pais/pais_list.html", {"paises": paises})


@csrf_exempt
def pais_manage(request, pais_id):
    if request.method == "GET":
        pais = Pais.get(pais_id)
        if not pais:
            return HttpResponse(status=400, content="País não encontrado")
        pais['nome'] = pais.get('nome_pais')
        return JsonResponse(pais, status=200)
    if request.method == "DELETE":
        estados = Estado.list(pais_id=pais_id)
        if estados:
            return HttpResponse(
                status=400,
                content="Não é possível remover um Pais que possui estados. Remova os estados primeiro.",
            )
        Pais.delete_from_id(pais_id)
        return HttpResponse(status=200)
    return HttpResponse(status=400, content="Método não permitido")


def estado_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        estado_id = str(data.pop("id", ""))
        if not data.get("nome_estado", False):
            return HttpResponse(status=400, content="Campos não preenchidos")

        pais = Pais.get(data["pais_id"])
        if not pais:
            return HttpResponse(status=400, content="País não encontrado.")

        if estado_id:
            Estado.update(estado_id, **data)
            return HttpResponse(status=200)

        estado_nome = data["nome_estado"]
        estados_existentes = Estado.list(nome_estado=estado_nome)
        if estados_existentes and (
            estados_existentes[0]["id"] != estado_id or not estado_id
        ):
            return HttpResponse(
                status=400, content="Já existe um Estado com esse nome cadastrado."
            )

        Estado.create(data)
        novo_estado = Estado.list()[-1]
        novo_estado['nome'] = novo_estado.get('nome_estado')
        return JsonResponse(novo_estado, status=200)

    estados = Estado.list()
    for index, estado in enumerate(estados):
        pais = Pais.get(estado["pais_id"])
        estados[index]["pais"] = pais["nome_pais"]
    paises = Pais.list()

    return render(
        request, "estado/estado_list.html", {"estados": estados, "paises": paises}
    )


@csrf_exempt
def cidade_from_estado(request, estado_id):
    if request.method != "GET":
        return HttpResponse(status=405)
    cidades = Cidade.list(estado_id=estado_id)
    return JsonResponse(cidades, safe=False)


@csrf_exempt
def estado_manage(request, estado_id):
    if request.method == "GET":
        estado = Estado.get(estado_id)
        if not estado:
            return HttpResponse(status=400, content="Estado não encontrado")
        estado["nome"] = estado.get("nome_estado")
        return JsonResponse(estado, status=200)
    if request.method == "DELETE":
        cidades = Cidade.list(estado_id=estado_id)
        if cidades:
            return HttpResponse(
                status=400,
                content="Não é possível remover um Estado que possui cidades. Remova as cidades primeiro.",
            )

        clientes = Cliente.list(estado_id=estado_id)
        if clientes:
            return HttpResponse(
                status=400,
                content=f"Não é possível remover um Estado que possui clientes. Remova os clientes primeiro: {', '.join([cliente['nome_cliente'] for cliente in clientes])}",
            )

        Estado.delete_from_id(estado_id)
        return HttpResponse(status=200)


def cidade_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        cidade_id = str(data.pop("id", ""))
        if not data.get("nome_cidade", False):
            return HttpResponse(status=400, content="Campos não preenchidos")

        if not data.get("ddd_cidade", False):
            return HttpResponse(status=400, content="Campos não preenchidos")

        estado = Estado.get(data["estado_id"])
        if not estado:
            return HttpResponse(status=400, content="Estado não encontrado.")

        cidade_nome = data["nome_cidade"]
        cidades_existentes = Cidade.list(nome_cidade=cidade_nome)

        if cidades_existentes and (
            not cidade_id or str(cidades_existentes[0]["id"]) != cidade_id
        ):
            return HttpResponse(
                status=400, content="Já existe uma Cidade com esse nome cadastrado."
            )

        if cidade_id:
            Cidade.update(cidade_id, **data)
            return HttpResponse(status=200)
        Cidade.create(data)
        nova_cidade = Cidade.list()[-1]
        nova_cidade['nome'] = nova_cidade.get('nome_cidade')
        return JsonResponse(nova_cidade, status=200)

    estados = Estado.list()
    cidades = Cidade.list()
    for index, cidade in enumerate(cidades):
        estado = Estado.get(cidade["estado_id"])
        cidades[index]["estado"] = estado["nome_estado"]
    paises = Pais.list()
    return render(
        request,
        "cidade/cidade_list.html",
        {"cidades": cidades, "estados": estados, "paises": paises},
    )


@csrf_exempt
def cidade_manage(request, cidade_id):
    if request.method == "DELETE":
        clientes = Cliente.list(cidade_id=cidade_id)
        if clientes:
            return HttpResponse(
                status=400,
                content=f"Não é possível remover uma Cidade que possui clientes. Remova os clientes primeiro: {', '.join([cliente['nome_cliente'] for cliente in clientes])}",
            )

        Cidade.delete_from_id(cidade_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        cidade = Cidade.get(cidade_id)
        if not cidade:
            return HttpResponse(status=400, content="Cidade não encontrada")
        cidade["nome"] = cidade.get("nome_cidade")
        return JsonResponse(cidade, status=200)
    return HttpResponse(status=400, content="Método não permitido")
