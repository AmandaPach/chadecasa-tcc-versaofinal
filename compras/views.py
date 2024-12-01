from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Compras, ComprasItem
from fornecedor.models import Fornecedor
from produtos.models import Produto, Categoria, TipoProduto
from pagamento.models import Pagamento, CondicaoPagamento, Modelo
from local.models import Cidade, Estado, Pais

from utils import to_date

def check_nota_fiscal(nota_fiscal, modelo_id, serie, fornecedor_id):
    # if Modelo.get(modelo_id) is None:
    #     return False

    compras_list = Compras.list(
        **{
            "nota_fiscal": nota_fiscal,
            "modelo_id": modelo_id,
            "serie": serie,
            "fornecedor_id": fornecedor_id,
        }
    )

    return bool(len(compras_list))

@csrf_exempt
def verify_nota(request):
    if request.method != "POST":
        return HttpResponse(status=405, content="Método não permitido.")

    nota_fiscal = int(request.POST.get("nota_fiscal"))
    modelo_id = int(request.POST.get("modelo"))
    serie = int(request.POST.get("serie"))
    fornecedor_id = int(request.POST.get("fornecedor"))

    if check_nota_fiscal(nota_fiscal, modelo_id, serie, fornecedor_id):
        return HttpResponse(
            status=400, content="Já existe nota fiscal com esses dados."
        )

    return HttpResponse(status=200, content="Nota fiscal válida.")

@csrf_exempt
def compra_cancelar(request):
    if request.method != "POST":
        return HttpResponse(status=405, content="Método não permitido.")
    data = request.POST
    nota_fiscal = int(data.get("nota_fiscal"))
    modelo_id = int(data.get("modelo"))
    serie = int(data.get("serie"))
    fornecedor_id = int(data.get("fornecedor_id"))
    compra = Compras.list(nota_fiscal=nota_fiscal, modelo_id=modelo_id, serie=serie, fornecedor_id=fornecedor_id)
    if not compra:
        return HttpResponse(status=404, content="Compra não encontrada.")
    
    query = F'''
        UPDATE compras SET cancelado = TRUE
        WHERE nota_fiscal = {nota_fiscal}
        AND modelo_id = {modelo_id}
        AND serie = {serie};
    '''
    Compras.mutation(query)

    compras_itens = ComprasItem.list(compra_nota_fiscal=nota_fiscal, compra_modelo_id=modelo_id, compra_serie=serie)
    for item in compras_itens:
        produto_id = item["produto_id"]
        quantidade = item["quantidade"]
        produto = Produto.get(produto_id)
        nova_quantidade = produto["quantidade"] - quantidade
        Produto.update(produto_id, **{"quantidade": nova_quantidade})
    return HttpResponse(status=200, content="Compra cancelada com sucesso.")

def compra_list(request):
    if request.method == "POST":
        data = dict(request.POST.lists())
        data.pop("csrfmiddlewaretoken")

        nota_fiscal = data.pop("nota_fiscal", True)[0]
        modelo_id = data.pop("modelo_id", True)[0]
        serie = data.pop("serie", True)[0]
        fornecedor_id = data.pop("fornecedor_id", True)[0]
        condicao_pagamento_id = data.pop("condicao_pagamento_id", True)[0]
        
        frete = data.pop("frete", True)[0]
        frete = frete.replace(",", ".").replace("R$", "")
        seguro = data.pop("seguro", True)[0]
        seguro = seguro.replace(",", ".").replace("R$", "")
        outras_despesas = data.pop("outras_despesas", True)[0]
        outras_despesas = outras_despesas.replace(",", ".").replace("R$", "")

        data_emissao = data.pop("data_emissao", True)[0]
        data_chegada = data.pop("data_chegada", True)[0]

        if not data_emissao or not data_chegada:
            return HttpResponse(status=400, content="Data inválida.")

        data_emissao = to_date(data_emissao)
        data_chegada = to_date(data_chegada)

        valor_total = float(data.pop("valor_total", True)[0])

        if check_nota_fiscal(nota_fiscal, modelo_id, serie, fornecedor_id):
            return HttpResponse(status=400, content="Compra já cadastrada.")

        if data_emissao > timezone.localtime():
            return HttpResponse(status=400, content="Data de emissão inválida.")

        if data_chegada < data_emissao:
            return HttpResponse(status=400, content="Data de chegada inválida.")

        Compras.create(
            {
                "nota_fiscal": nota_fiscal,
                "modelo_id": modelo_id,
                "serie": serie,
                "fornecedor_id": fornecedor_id,
                "frete": frete,
                "seguro": seguro,
                "outras_despesas": outras_despesas,
                "valor_total": valor_total,
                "data_emissao": data_emissao,
                "data_chegada": data_chegada,
                "condicao_pagamento_id": condicao_pagamento_id,
            }
        )

        ultima_compra = Compras.list()[-1]
        compra_id = {
            "compra_nota_fiscal": nota_fiscal,
            "compra_modelo_id": modelo_id,
            "compra_serie": serie,
            "compra_fornecedor_id": fornecedor_id,
        }

        for i in range(len(data["produto_id"])):
            produto_id = data["produto_id"][i]
            quantidade = data["quantidade"][i]
            custo = data["custo"][i]
            desconto = data["desconto"][i]

            ComprasItem.create(
                {
                    "produto_id": produto_id,
                    "quantidade": quantidade,
                    "custo": custo,
                    "desconto": desconto,
                    **compra_id,
                }
            )

            produto = Produto.get(produto_id)
            nova_quantidade = produto["quantidade"] + int(quantidade)
            Produto.update(produto_id, **{"quantidade": nova_quantidade})
        return JsonResponse(ultima_compra, status=200)

    compras_list = Compras.list()
    for i, compra in enumerate(compras_list):
        fornecedor_id = compra["fornecedor_id"]
        fornecedor = Fornecedor.get(fornecedor_id)
        if fornecedor:
            compras_list[i]["fornecedor_nome"] = fornecedor["nome_fantasia_fornecedor"]

    fornecedores = Fornecedor.list(status=True)
    produtos = Produto.list()
    categorias = Categoria.list(status=True)
    tipos = TipoProduto.list(status=True, compravel=True)
    forma_pagamento = Pagamento.list(status=True)
    condicao_pagamento = CondicaoPagamento.list()
    cidades = Cidade.list()
    estados = Estado.list()
    paises = Pais.list()
    modelos = Modelo.list(status=True)

    return render(
        request,
        "compras/compra_list.html",
        {
            "compras": compras_list,
            "fornecedores": fornecedores,
            "produtos": produtos,
            "categorias": categorias,
            "tipos": tipos,
            "forma_pagamentos": forma_pagamento,
            "condicoes": condicao_pagamento,
            "cidades": cidades,
            "estados": estados,
            "paises": paises,
            "modelos": modelos,
        },
    )

@csrf_exempt
def compra_manage(request):
    if request.method == "POST":
        data = dict(request.POST.lists())
        nota_fiscal = data.pop("nota_fiscal", [False])[0]
        modelo_id = data.pop("modelo", [False])[0]
        serie = data.pop("serie", [False])[0]
        fornecedor = data.pop("fornecedor_id", [False])[0]

        if not all([nota_fiscal, modelo_id, serie, fornecedor]):
            return HttpResponse(status=400, content="Dados inválidos.")

        if not check_nota_fiscal(nota_fiscal, modelo_id, serie, fornecedor):
            return HttpResponse(status=400, content="Compra não registrada.")
        
        compra = Compras.list(nota_fiscal=nota_fiscal, modelo_id=modelo_id, serie=serie)[0]
        compras_item = ComprasItem.list(compra_nota_fiscal=nota_fiscal, compra_modelo_id=modelo_id, compra_serie=serie)
        for item in compras_item:
            produto = Produto.get(item["produto_id"])
            item["produto"] = produto['nome_produto']
        compra['itens'] = compras_item

        return JsonResponse(compra, status=200)
    return HttpResponse(status=405, content="Método não permitido.")

def categoria_list(request):
    if request.method == "POST":
        data = request.POST
        data.pop("csrfmiddlewaretoken")
        Categoria.create(data)
        return redirect("compras:categoria_list")

    categorias = Categoria.list()
    return render(
        request,
        "compras/categoria_list.html",
        {
            "categorias": categorias,
        },
    )
