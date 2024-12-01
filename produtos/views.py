from webbrowser import get
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Produto, Categoria, TipoProduto
from compras.models import ComprasItem
from vendas.models import VendasItem

from utils import process_form_data

def calcula_preco_medio(produto_id):
    compras = get_produtos_ativos_compras(produto_id)
    vendas = get_produtos_ativos_vendas(produto_id)
    produto = Produto.get(produto_id)
    produto_preco = produto['preco_custo_produto']
    produto_preco = float(str(produto_preco).replace("R$ ", "").replace(",", "."))
    format_value = lambda value: float(str(value).replace("R$ ", "").replace(",", "."))
    if not compras:
        return produto_preco
    total_quantidade = 0
    total_custo = 0
    for compra in compras:
        total_quantidade += format_value(compra["quantidade"])
        total_custo += format_value(compra["custo"]) * format_value(compra["quantidade"])
    total_quantidade -= len(vendas)
    custo_medio = total_custo / total_quantidade if total_quantidade else produto_preco
    return custo_medio

def get_produtos_ativos_compras(produto_id):
    query = f'''
        SELECT * 
        FROM compras_item 
        WHERE produto_id = {produto_id}
        AND (compra_nota_fiscal, compra_modelo_id, compra_serie) 
            NOT IN (
                SELECT nota_fiscal, modelo_id, serie 
                FROM compras 
                WHERE cancelado = TRUE
            );
    '''

    return Produto.query(query)

def get_produtos_ativos_vendas(produto_id):
    query = f'''
        SELECT * 
        FROM vendas_item 
        WHERE produto_id = {produto_id}
        AND (venda_nota_fiscal, venda_modelo_nota, venda_serie) 
            NOT IN (
                SELECT nota_fiscal, modelo_nota, serie 
                FROM vendas 
                WHERE cancelado = TRUE
            );
    '''

    return Produto.query(query)

@csrf_exempt
def product_check(request):
    if request.method != "POST":
        return HttpResponse(status=400, content="Método não permitido")
    data = request.POST
    produtos = data.get("produtos", [])
    produtos = json.loads(produtos)
    for produto in produtos:
        if not produto:
            continue
        produto_id = produto.get("produto")
        produto_quantidade = produto.get("quantidade")
        produto = Produto.get(produto_id)
        if produto.get("quantidade") < int(produto_quantidade):
            return HttpResponse(
                status=400,
                content=f"Quantidade insuficiente no estoque para o produto {produto.get('nome_produto')}",
            )
    return HttpResponse(status=200, content="Nenhum produto informado")


def produto_options(request):
    if request.method != "GET":
        return HttpResponse(status=400, content="Método não permitido")
    vendas = request.GET.get("venda", False)
    compras = request.GET.get("compra", False)
    quantidade = request.GET.get("quantidade", False)
    outer_clause = []
    where_clause = []
    if vendas:
        where_clause.append("(vendavel = 'True' OR vendavel = TRUE)")
    if compras:
        where_clause.append("(compravel = 'True' OR compravel = TRUE)")
    if quantidade:
        outer_clause.append("produto.quantidade > 0")
    where_clause = " AND ".join(where_clause)
    outer_clause = " AND ".join(outer_clause) + " AND " if outer_clause else ""
    query = f'''
        SELECT *
        FROM produto
        WHERE {outer_clause} produto.tipo_id in (
            SELECT id FROM tipo_produto WHERE {where_clause}
        )'''
    produtos = Produto.query(query)
    for index, produto in enumerate(produtos):
        nome_produto = produto["nome_produto"]
        id_produto = produto["id"]
        produtos[index] = {"id": id_produto, "nome": nome_produto}
    return JsonResponse(produtos, status=200, safe=False)


def produto_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        produto_id = str(data.pop("id", ""))
        data.pop("data_cadastro", True)
        data.pop("data_ultima_alteracao", True)
        descricao = data.pop("descricao_produto", "")
        if not all(data.values()):
            return HttpResponse("Campo obrigatório não preenchido", status=400)

        produto_nome = data["nome_produto"]
        produtos = Produto.list(nome_produto=produto_nome)
        if produtos and (not produto_id or str(produtos[0]["id"]) != produto_id):
            return HttpResponse(
                status=400, content=f'Produto "{produto_nome}" já cadastrado'
            )

        if produto_id:
            Produto.update(produto_id, **data)
            return HttpResponse(status=200)

        Produto.create({**data, "descricao_produto": descricao})
        new_produto = Produto.list()[-1]
        new_produto["nome"] = new_produto.get("nome_produto")
        return JsonResponse(new_produto, status=200)

    categorias = Categoria.list(status=True)
    tipos = TipoProduto.list(status=True)
    produtos = Produto.list()

    
    for index, produto in enumerate(produtos):
        custo_medio = calcula_preco_medio(produto["id"])
        produtos[index]["preco_medio"] = f"R$ {custo_medio:.2f}" if custo_medio else None

        categoria = Categoria.list(id=produto["categoria_id"])
        if categoria:
            categoria = categoria[0]
            produtos[index]["categoria_nome"] = categoria["nome_categoria"]

        tipo = TipoProduto.list(id=produto["tipo_id"])
        if tipo:
            tipo = tipo[0]
            produtos[index]["tipo_nome"] = tipo["nome_tipo"]

        unidade_medida = produto["unid_medida_produto"]

        unidade_map = {
            "UN": "Unidade",
            "KG": "Quilograma",
            "LT": "Litro",
        }
        unidade_medida = unidade_map.get(unidade_medida, unidade_medida)
        produtos[index]["unid_medida_produto"] = unidade_medida

    return render(
        request,
        "produtos/produto_list.html",
        {"produtos": produtos, "categorias": categorias, "tipos": tipos},
    )


@csrf_exempt
def produto_manage(request, produto_id):
    if request.method == "DELETE":
        compra_query = f'''
        SELECT *
        FROM compras_item
        WHERE produto_id = {produto_id}
        AND (compra_nota_fiscal, compra_modelo_id, compra_serie, compra_fornecedor_id) NOT IN (
            SELECT nota_fiscal, modelo_id, serie, fornecedor_id
            FROM compras
            WHERE cancelado = True or cancelado = TRUE
        );
        '''
        compras = ComprasItem.query(compra_query)
        if compras:
            return HttpResponse(
                status=400, content="Existem compras vinculadas a este produto"
            )
        vendas = VendasItem.list(produto_id=produto_id)
        if vendas:
            return HttpResponse(
                status=400, content="Existem vendas vinculadas a este produto"
            )
        Produto.delete_from_id(produto_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        produto = Produto.get(produto_id)
        if not produto:
            return HttpResponse(status=400, content="Produto não encontrado")
        preco_medio = calcula_preco_medio(produto_id)
        produto["preco_medio"] = f"R$ {preco_medio:.2f}" if preco_medio else None
        
        produto['nome'] = produto.get('nome_produto')
        if produto["categoria_id"]:
            categoria = Categoria.get(produto["categoria_id"])
            if categoria:
                produto["categoria"] = categoria["nome_categoria"]
        if produto["tipo_id"]:
            tipo = TipoProduto.get(produto["tipo_id"])
            if tipo:
                produto["tipo"] = tipo["nome_tipo"]
                produto["vendavel"] = tipo["vendavel"]
                produto["compravel"] = tipo["compravel"]
        compras = get_produtos_ativos_compras(produto_id)
        vendas = get_produtos_ativos_vendas(produto_id)
        produto["bloqueado"] = bool(vendas or compras)
        return JsonResponse(produto, status=200)

    return HttpResponse(status=400, content="Método não permitido")


def categoria_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data["status"] = data.get("status", "") == "on"
        categoria_id = data.pop("id", "")

        categoria_nome = data["nome_categoria"]
        if not categoria_nome:
            return HttpResponse("Campo obrigatório não preenchido", status=400)

        categorias = Categoria.list(nome_categoria=categoria_nome)
        if categorias and (
            not categoria_id or str(categorias[0]["id"]) != str(categoria_id)
        ):
            return HttpResponse(
                status=400, content=f'Categoria "{categoria_nome}" já cadastrada'
            )

        if categoria_id:
            Categoria.update(categoria_id, **data)
            return HttpResponse(status=200)

        Categoria.create(data)
        new_categoria = Categoria.list()[-1]
        new_categoria["nome"] = new_categoria.get("nome_categoria")
        return JsonResponse(new_categoria, status=200)

    categorias = Categoria.list()
    return render(request, "produtos/categoria_list.html", {"categorias": categorias})


@csrf_exempt
def categoria_manage(request, categoria_id):
    if request.method == "DELETE":
        produtos = Produto.list(categoria_id=categoria_id)
        if produtos:
            return HttpResponse(
                status=400, content="Existem produtos vinculados a esta categoria"
            )

        Categoria.delete_from_id(categoria_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        categoria = Categoria.get(categoria_id)
        if not categoria:
            return HttpResponse(status=400, content="Categoria não encontrada")
        categoria['nome'] = categoria.get('nome_categoria')
        return JsonResponse(categoria, status=200)
    return HttpResponse(status=400, content="Método não permitido")


def tipo_produto_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        tipo_id = str(data.pop("id", ""))
        data["status"] = data.get("status", "") == "on"
        data["vendavel"] = data.get("vendavel", "") == "on"
        data["compravel"] = data.get("compravel", "") == "on"

        tipo_nome = data["nome_tipo"]
        tipos = TipoProduto.list(nome_tipo=tipo_nome)
        if tipos and (not tipo_id or str(tipos[0]["id"]) != str(tipo_id)):
            return HttpResponse(
                status=400, content=f'Tipo de produto "{tipo_nome}" já cadastrado'
            )

        if tipo_id:
            TipoProduto.update(tipo_id, **data)
            return HttpResponse(status=200)

        TipoProduto.create(data)
        new_produto = TipoProduto.list()[-1]
        new_produto["nome"] = new_produto.get("nome_tipo")
        return JsonResponse(new_produto, status=200)

    tipos_produtos = TipoProduto.list()
    return render(
        request, "produtos/tipo_produto_list.html", {"tipos_produtos": tipos_produtos}
    )


@csrf_exempt
def tipo_produto_manage(request, tipo_produto_id):
    if request.method == "DELETE":
        produtos = Produto.list(tipo_id=tipo_produto_id)
        if produtos:
            return HttpResponse(
                status=400, content="Existem produtos vinculados a este tipo de produto"
            )

        TipoProduto.delete_from_id(tipo_produto_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        tipo_produto = TipoProduto.get(tipo_produto_id)
        if not tipo_produto:
            return HttpResponse(status=400, content="Tipo de produto não encontrado")
        tipo_produto['nome'] = tipo_produto.get('nome_tipo')
        return JsonResponse(tipo_produto, status=200)

    return HttpResponse(status=400, content="Método não permitido")