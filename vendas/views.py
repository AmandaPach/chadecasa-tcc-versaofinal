from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Vendas, VendasItem
from cliente.models import Cliente
from produtos.models import Produto, Categoria, TipoProduto
from pagamento.models import Pagamento, CondicaoPagamento, Modelo
from local.models import Cidade, Estado, Pais

#verificar se já existe uma nota com os mesmo parametros
def check_nota_fiscal(nota_fiscal, modelo_nota, serie, cliente_id):
    vendas_list = Vendas.list(
        **{
            "nota_fiscal": nota_fiscal,
            "modelo_nota": modelo_nota,
            "serie": serie,
            "cliente_id": cliente_id,
        }
    )

    return bool(len(vendas_list))

@csrf_exempt
def verify_nota(request):
    if request.method != "POST":
        return HttpResponse(status=405, content="Método não permitido.")
    
    nota_fiscal = int(request.POST.get("nota_fiscal"))
    modelo_nota = int(request.POST.get("modelo"))
    serie = int(request.POST.get("serie"))
    fornecedor_id = int(request.POST.get("fornecedor"))

    if check_nota_fiscal(nota_fiscal, modelo_nota, serie, fornecedor_id):
        return HttpResponse(
            status=400, content="Já existe nota fiscal com esses dados."
        )
    
    return HttpResponse(status=200, content="Nota fiscal válida.")

# cancelar venda
@csrf_exempt
def venda_cancelar(request):
    if request.method != "POST":
        return HttpResponse(status=405, content="Método não permitido.")
    data = request.POST
    nota_fiscal = int(data.get("nota_fiscal"))
    modelo_nota = int(data.get("modelo"))
    serie = int(data.get("serie"))
    cliente_id = int(data.get("cliente_id"))
    venda = Vendas.list(nota_fiscal=nota_fiscal, modelo_nota=modelo_nota, serie=serie, cliente_id=cliente_id)
    if not venda:
        return HttpResponse(status=404, content="Venda não encontrada.")
    
    query = F'''
        UPDATE vendas SET cancelado = TRUE
        WHERE nota_fiscal = {nota_fiscal}
        AND modelo_nota = {modelo_nota}
        AND serie = {serie}
        AND cliente_id = {cliente_id}
    '''
    Vendas.mutation(query)

    vendas_itens = VendasItem.list(venda_nota_fiscal=nota_fiscal, venda_modelo_nota=modelo_nota, venda_serie=serie, venda_cliente_id=cliente_id)
    for item in vendas_itens:
        produto = Produto.get(item["produto_id"])
        nova_quantidade = produto['quantidade'] + item['quantidade']
        Produto.update(id=item['produto_id'], quantidade=nova_quantidade)
    return HttpResponse(status=200, content="Venda cancelada.")


def venda_list(request):
    if request.method == "POST":
        data = dict(request.POST.lists())
        data.pop("csrfmiddlewaretoken")

        modelo_nota = 65
        serie = 31
        cliente_id = data.pop("cliente_id", [False])[0]
        condicao_id = data.pop("condicao_pagamento_id", [False])[0]

        frete = data.pop("frete", True)[0]
        frete = frete.replace(",", ".").replace("R$", "")
        seguro = data.pop("seguro", True)[0]
        seguro = seguro.replace(",", ".").replace("R$", "")
        outras_despesas = data.pop("outras_despesas", True)[0]
        outras_despesas = outras_despesas.replace(",", ".").replace("R$", "")

        valor_total = float(data.pop("valor_total", True)[0])
        
        ultima_venda = Vendas.list()
        nota_fiscal = 1
        if ultima_venda:
            nota_fiscal = ultima_venda[-1]['nota_fiscal'] + 1
        if nota_fiscal > 1000000:
            nota_fiscal = 1

        Vendas.create(
            {
                "nota_fiscal": nota_fiscal,
                "modelo_nota": modelo_nota,
                "serie": serie,
                "cliente_id": cliente_id,
                "condicao_pagamento_id": condicao_id,
                "valor_total": valor_total,
                "frete": frete,
                "seguro": seguro,
                "outras_despesas": outras_despesas,
            }
        )

        for i in range(len(data['produto_id'])):
            produto_id = data['produto_id'][i]
            quantidade = data['quantidade'][i]
            custo = data['custo'][i]
            desconto = data['desconto'][i]

            VendasItem.create(
                {
                    "produto_id": produto_id,
                    "quantidade": quantidade,
                    "valor_unitario": custo,
                    "desconto": desconto,
                    "venda_nota_fiscal": nota_fiscal,
                    "venda_modelo_nota": modelo_nota,
                    "venda_serie": serie,
                    "venda_cliente_id": cliente_id,
                }
            )

            produto = Produto.get(produto_id)
            nova_quantidade = produto['quantidade'] - int(quantidade)
            if nova_quantidade < 0:
                return HttpResponse(status=400, content=f"Quantidade insuficiente em estoque do produto {produto['nome_produto']}.")
            Produto.update(**{"id": produto['id'], "quantidade": nova_quantidade})
        return JsonResponse(ultima_venda, status=200, safe=False)

    vendas = Vendas.list()
    for i, venda in enumerate(vendas):
        cliente_id = venda['cliente_id']
        condicao_id = venda['condicao_pagamento_id']
        condicao = CondicaoPagamento.get(condicao_id)
        vendas[i]['condicao_pagamento'] = condicao['nome_condicao_pgto']
        cliente = Cliente.get(cliente_id)
        if cliente:
            vendas[i]['cliente_nome'] = cliente['nome_cliente']
        vendas[i]['valor_total'] = f"{venda['valor_total']:.2f}".replace(".", ",")
    
    clientes = Cliente.list(status=True, apagado=False)
    produtos_query = "SELECT * FROM produto WHERE produto.quantidade != 0 and tipo_id not in (select id from tipo_produto where vendavel = False or vendavel = FALSE or vendavel = 0)"
    produtos = Produto.query(produtos_query)
    print(produtos)
    categorias = Categoria.list(status=True)
    tipos = TipoProduto.list(status=True)
    forma_pagamento = Pagamento.list(status=True)
    condicao_pagamento = CondicaoPagamento.list()
    cidades = Cidade.list()
    estados = Estado.list()
    paises = Pais.list()

    return render(
        request,
        "vendas/venda_list.html",
        {
            "vendas": vendas,
            "clientes": clientes,
            "produtos": produtos,
            "categorias": categorias,
            "tipos": tipos,
            "forma_pagamento": forma_pagamento,
            "condicoes": condicao_pagamento,
            "cidades": cidades,
            "estados": estados,
            "paises": paises,
        }
    )

@csrf_exempt
def venda_manage(request):
    if request.method == "POST":
        data = dict(request.POST.lists())
        nota_fiscal = data.pop("nota_fiscal", [False])[0]
        modelo_nota = data.pop("modelo", [False])[0]
        serie = data.pop("serie", [False])[0]
        cliente_id = data.pop("cliente_id", [False])[0]

        if not all([nota_fiscal, modelo_nota, serie, cliente_id]):
            return HttpResponse(status=400, content="Dados inválidos.")
        
        venda = Vendas.list(
            nota_fiscal=nota_fiscal,
            modelo_nota=modelo_nota,
            serie=serie,
            cliente_id=cliente_id,
        )[0]
        venda_items = VendasItem.list(
            venda_nota_fiscal=nota_fiscal,
            venda_modelo_nota=modelo_nota,
            venda_serie=serie,
            venda_cliente_id=cliente_id,
        )
        for i, item in enumerate(venda_items):
            produto = Produto.get(item["produto_id"])
            venda_items[i]['produto'] = produto.get("nome_produto")

        venda["itens"] = venda_items

        return JsonResponse(venda, status=200)
    return HttpResponse(status=405, content="Método não permitido.")