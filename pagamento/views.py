from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Pagamento, CondicaoPagamento, Parcela, Modelo
from compras.models import Compras
from utils import process_form_data
import re

from compras.models import Compras

@csrf_exempt
def pagamento_options(request):
    if request.method != "GET":
        return HttpResponse(status=400, content="Método não permitido")
    pagamentos = Pagamento.list(status=True)
    for index, pagamento in enumerate(pagamentos):
        nome_pagamento = pagamento["nome_pagamento"]
        id_pagamento = pagamento["id"]
        pagamentos[index] = {"id": id_pagamento, "nome": nome_pagamento}
    return JsonResponse(pagamentos, status=200, safe=False)


def pagamento_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data["status"] = data.get("status", "") == "on"
        pagamento_id = str(data.pop("id", ""))

        if not data.get("nome_pagamento"):
            return HttpResponse("Campo obrigatório não preenchido", status=400)

        pagamento_existente = Pagamento.list(nome_pagamento=data["nome_pagamento"])
        if pagamento_existente and (
            str(pagamento_existente[0]["id"]) != pagamento_id or not pagamento_id
        ):
            return HttpResponse(
                status=400,
                content="Já existe uma forma de pagamento com esse nome cadastrado.",
            )

        if pagamento_id:
            Pagamento.update(pagamento_id, **data)
            return HttpResponse(status=200)

        Pagamento.create(data)
        new_pagamento = Pagamento.list()[-1]
        new_pagamento["nome"] = new_pagamento.get("nome_pagamento")
        return JsonResponse(new_pagamento, status=200)
    pagamentos = Pagamento.list()
    return render(
        request, "pagamento/forma_pagamento_list.html", {"pagamentos": pagamentos}
    )


@csrf_exempt
def pagamento_manage(request, pagamento_id):
    if request.method == "DELETE":
        parcelas = Parcela.list(forma_pgto_id=pagamento_id)
        if parcelas:
            return HttpResponse(
                status=400,
                content="Não é possível excluir uma forma de pagamento que está vinculada a uma condição de pagamento.",
            )
        Pagamento.delete_from_id(pagamento_id)

    if request.method == "GET":
        pagamento = Pagamento.get(pagamento_id)
        if not pagamento:
            return HttpResponse(status=400, content="Forma de pagamento não encontrada")
        pagamento['nome'] = pagamento.get('nome_pagamento')
        return JsonResponse(pagamento, status=200)

    return HttpResponse(status=400, content="Método não permitido")


def condicao_pagamento_list(request):
    if request.method == "POST":
        data_lists = dict(request.POST.lists())
        data_lists.pop("csrfmiddlewaretoken")
        data_lists["status"] = data_lists.get("status", "") == "on"
        nome = data_lists.pop("nome_condicao_pgto", False)[0]
        condicao_pagamento_id = str(data_lists.pop("id", [""])[0])
        if not nome:
            return HttpResponse(status=400, content="Campo obrigatório não preenchido.")

        parcelas_count = len(data_lists["parcela"])

        existente_condicao = CondicaoPagamento.list(nome_condicao_pgto=nome)
        if existente_condicao and (
            not condicao_pagamento_id or str(existente_condicao[0]["id"]) != condicao_pagamento_id
        ):
            return HttpResponse(
                status=400, content="Já existe uma condição de pagamento com esse nome."
            )

        required_colunas = [
            ("Parcela", "parcela"),
            ("Dias", "dias"),
            ("Percentual", "percentual"),
            ("Desconto", "desconto"),
            ("Taxa", "taxa"),
            ("Multa", "multa"),
            ("Forma de Pagamento", "forma_pagamento"),
        ]

        for coluna, key in required_colunas:
            if key not in data_lists:
                return HttpResponse(
                    status=400, content=f"Campo {coluna} é obrigatório."
                )

        if condicao_pagamento_id:
            compras = Compras.list(condicao_pagamento_id=condicao_pagamento_id)
            if compras:
                return HttpResponse(
                    status=400,
                    content="Não é possível editar uma condição de pagamento que está vinculada a uma compra."
                )
            CondicaoPagamento.update(
                condicao_pagamento_id, nome_condicao_pgto=nome, parcela=parcelas_count
            )
            Parcela.delete(condicao_pgto_id=condicao_pagamento_id)

        CondicaoPagamento.create(
            {
                "nome_condicao_pgto": nome,
                "parcela": parcelas_count,
            }
        )
        new_condicao_pagamento = CondicaoPagamento.list()[-1]
        new_condicao_pagamento["nome"] = new_condicao_pagamento.get("nome_condicao_pgto")

        clean_porcentagem = lambda x: re.sub(r"[^\d,]", "", x)
        for i in range(len(data_lists["parcela"])):
            porcentagem = clean_porcentagem(data_lists["percentual"][i])
            parcela = {
                "numero_parcela": data_lists["parcela"][i],
                "dia_pgto_parcela": data_lists["dias"][i],
                "porcentagem_pgto_parcela": porcentagem,
                "desconto_pgto_parcela": data_lists["desconto"][i],
                "juros_pgto_parcela": data_lists["taxa"][i],
                "multa_pgto_parcela": data_lists["multa"][i],
                "forma_pgto_id": data_lists["forma_pagamento"][i],
                "condicao_pgto_id": new_condicao_pagamento["id"],
            }
            Parcela.create(parcela)

        if "id" in data_lists:
            return HttpResponse(status=200)

        return JsonResponse(new_condicao_pagamento, status=200)

    condicoes = CondicaoPagamento.list()
    for i, condicao in enumerate(condicoes):
        parcelas = Parcela.list(condicao_pgto_id=condicao["id"])
        condicao["parcelas"] = parcelas
        condicoes[i] = condicao
    pagamentos = Pagamento.list(status=True)
    return render(
        request,
        "pagamento/condicao_pagamento_list.html",
        {"condicoes": condicoes, "pagamentos": pagamentos},
    )


@csrf_exempt
def condicao_pagamento_manage(request, condicao_pagamento_id):
    if request.method == "GET":
        condicao_pagamento = CondicaoPagamento.get(condicao_pagamento_id)
        if not condicao_pagamento:
            return HttpResponse(
                status=400, content="Condição de pagamento não encontrada"
            )
        condicao_pagamento['nome'] = condicao_pagamento.get('nome_condicao_pgto')
        parcelas = Parcela.list(condicao_pgto_id=condicao_pagamento_id)
        for i, parcela in enumerate(parcelas):
            forma_pagamento = Pagamento.get(parcela["forma_pgto_id"])
            parcelas[i]["forma_pagamento"] = forma_pagamento["nome_pagamento"]
        condicao_pagamento["parcelas"] = parcelas
        return JsonResponse(condicao_pagamento, status=200)

    if request.method == "DELETE":
        if Compras.list(condicao_pagamento_id=condicao_pagamento_id):
            return HttpResponse(
                status=400,
                content="Não é possível excluir uma condição de pagamento que está vinculada a uma compra."
            )
        CondicaoPagamento.delete_from_id(condicao_pagamento_id)
        return HttpResponse(status=200)

    return HttpResponse(status=400, content="Método não permitido")


def modelo_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data["status"] = data.get("status", "") == "on"
        data.pop("data_cadastro", "")
        data.pop("data_ultima_alteracao", "")
        modelo_id = str(data.pop("id", ""))

        if not data.get("numero_modelo"):
            return HttpResponse("Campo obrigatório não preenchido", status=400)
        
        

        modelo_existente = Modelo.list(numero_modelo=data["numero_modelo"])
        if modelo_existente and (
            str(modelo_existente[0]["id"]) != modelo_id or not modelo_id
        ):
            return HttpResponse(
                status=400,
                content="Já existe um modelo de nota fiscal com esse número.",
            )

        if modelo_id:
            compras_list = Compras.list(modelo_id=modelo_id)
            if compras_list:
                return HttpResponse(
                    status=400,
                    content="Não é possível editar um modelo de nota fiscal que está vinculado a uma compra."
                )
            Modelo.update(modelo_id, **data)
            return HttpResponse(status=200)

        Modelo.create(data)
        new_modelo = Modelo.list()[-1]
        return JsonResponse(new_modelo, status=200)
    modelos = Modelo.list()
    return render(
        request, "pagamento/modelo_list.html", {"modelos": modelos}
    )

@csrf_exempt
def modelo_options(request):
    if request.method != "GET":
        return HttpResponse(status=400, content="Método não permitido")
    modelos = Modelo.list()
    for index, modelo in enumerate(modelos):
        numero_modelo = modelo["numero_modelo"]
        modelos[index] = {"numero": numero_modelo}
    return JsonResponse(modelos, status=200, safe=False)


@csrf_exempt
def modelo_manage(request, modelo_id):
    if request.method == "GET":
        modelo = Modelo.get(modelo_id)
        if not modelo:
            return HttpResponse(status=400, content="Modelo de nota fiscal não encontrada")
        return JsonResponse(modelo, status=200)

    if request.method == "DELETE":
        Modelo.delete_from_id(modelo_id)
        compras_list = Compras.list(modelo_id=int(modelo_id))
        if compras_list:
            return HttpResponse(
                status=400,
                content="Não é possível editar um modelo de nota fiscal que está vinculado a uma compra."
            )
        return HttpResponse(status=200)

    return HttpResponse(status=405, content="Método não permitido")
