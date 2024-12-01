from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Fornecedor
from local.models import Cidade, Estado, Pais
from compras.models import Compras
from utils import process_form_data, validar_cnpj

required_fields = [
    "nome_fantasia_fornecedor",
    "razao_social_fornecedor",
    "cnpj_fornecedor",
    "rua_fornecedor",
    "bairro_fornecedor",
    "telefone_fornecedor",
    "numero_rua_fornecedor",
    "cep_fornecedor",
    "cidade_id",
]


def fornecedor_list(request):
    if request.method == "POST":
        data = process_form_data(request.POST)
        data["status"] = data.get("status", "") == "on"
        fornecedor_id = str(data.pop("id", ""))

        for field in required_fields:
            if not data.get(field):
                return HttpResponse(f"Campo obrigatório não preenchido", status=400)

        data_fundacao = data.get("data_fundacao_fornecedor")
        if data_fundacao:
            if len(data_fundacao) != 10:
                return HttpResponse("Data de fundação inválida", status=400)
            today_date = timezone.now().strftime("%Y-%m-%d")
            if data_fundacao > today_date:
                return HttpResponse(
                    "Data de fundação não pode ser maior que a data atual", status=400
                )

        fornecedor_nome = data.get("nome_fantasia_fornecedor")
        razao_social = data.get("razao_social_fornecedor")
        nome_fantasia = data.get("nome_fantasia_fornecedor")
        cnpj = data.get("cnpj_fornecedor")
        ie = data.get("ie_fornecedor")

        if not validar_cnpj(cnpj):
            return HttpResponse(
                "CNPJ inválido. Verifique e tente novamente", status=400
            )

        unique_fields = {
            "nome_fantasia_fornecedor": ("Nome", fornecedor_nome),
            "razao_social_fornecedor": ("Razão Social", razao_social),
            "nome_fantasia_fornecedor": ("Nome Fantasia", nome_fantasia),
            "cnpj_fornecedor": ("CNPJ", cnpj),
            "ie_fornecedor": ("Inscrição Estadual", ie),
        }

        for field, (field_name, field_value) in unique_fields.items():
            unique_lista = Fornecedor.list(**{field: field_value})
            if unique_lista and (
                not fornecedor_id or str(unique_lista[0]["id"]) != fornecedor_id
            ):
                return HttpResponse(
                    f'{field_name} "{field_value}" já cadastrado', status=400
                )

        if fornecedor_id:
            Fornecedor.update(fornecedor_id, **data)
            return HttpResponse(status=200)

        cidade_id = data.get("cidade_id")
        cidade = Cidade.get(cidade_id)
        estado_id = cidade.get("estado_id")
        data["estado_id"] = estado_id

        Fornecedor.create(data)
        new_fornecedor = Fornecedor.list()[-1]
        cidade_id = new_fornecedor.get("cidade_id")
        new_fornecedor["cidade"] = Cidade.get(cidade_id)["nome_cidade"]
        new_fornecedor["nome"] = new_fornecedor.get("nome_fantasia_fornecedor")
        return JsonResponse(new_fornecedor, status=200)

    estados = Estado.list()
    cidades = Cidade.list()
    paises = Pais.list()
    fornecedores = Fornecedor.list()
    for i, fornecedor in enumerate(fornecedores):
        cidade_id = fornecedor.get("cidade_id")
        estado_id = fornecedor.get("estado_id")
        fornecedor["cidade"] = Cidade.get(cidade_id)["nome_cidade"]
        fornecedor["estado"] = Estado.get(estado_id)["nome_estado"]
        fornecedores[i] = fornecedor

    return render(
        request,
        "fornecedor/fornecedor_list.html",
        {
            "estados": estados,
            "cidades": cidades,
            "paises": paises,
            "fornecedores": fornecedores,
        },
    )


@csrf_exempt
def manage(request, fornecedor_id):
    if request.method == "DELETE":
        compras_list = Compras.list(fornecedor_id=fornecedor_id)
        if compras_list:
            return HttpResponse(
                "Fornecedor não pode ser excluído, pois possui compras cadastradas",
                status=400,
            )

        Fornecedor.delete_from_id(fornecedor_id)
        return HttpResponse(status=200)

    if request.method == "GET":
        fornecedor = Fornecedor.get(fornecedor_id)
        if not fornecedor:
            return HttpResponse(status=400, content="Fornecedor não encontrado")
        fornecedor['nome'] = fornecedor.get('nome_fantasia_fornecedor')
        cidade_id = fornecedor.get("cidade_id")
        estado_id = fornecedor.get("estado_id")
        cidade = Cidade.get(cidade_id) if cidade_id else None
        estado = Estado.get(estado_id) if estado_id else None
        fornecedor["cidade"] = cidade["nome_cidade"]
        fornecedor["estado"] = estado["nome_estado"]
        return JsonResponse(fornecedor, status=200)
    return HttpResponse(status=400, content="Método não permitido")
