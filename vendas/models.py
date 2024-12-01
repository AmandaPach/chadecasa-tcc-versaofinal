from database.db import Table

# Create your models here.
vendas_columns = {
    "nota_fiscal": "INTEGER NOT NULL",
    "modelo_nota": "INTEGER NOT NULL DEFAULT 55",
    "serie": "INTEGER NOT NULL DEFAULT 1",
    "cliente_id": "INTEGER NOT NULL",
    "condicao_pagamento_id": "INTEGER NOT NULL",
    "frete": "INTEGER NOT NULL DEFAULT 0",
    "seguro": "INTEGER NOT NULL DEFAULT 0",
    "outras_despesas": "INTEGER NOT NULL DEFAULT 0",
    "cancelado": "BOOLEAN NOT NULL DEFAULT FALSE",
    "valor_total": "INTEGER NOT NULL",
    "data_venda": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_emissao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}


Vendas = Table(
    "vendas", vendas_columns, primary_keys=["nota_fiscal", "modelo_nota", "serie", "cliente_id"]
)

vendas_item_columns = {
    "quantidade": "INTEGER NOT NULL",
    "valor_unitario": "INTEGER NOT NULL",
    "desconto": "INTEGER NOT NULL",
    "produto_id": "INTEGER NOT NULL",
    "venda_nota_fiscal": "INTEGER NOT NULL",
    "venda_modelo_nota": "INTEGER NOT NULL DEFAULT 55",
    "venda_serie": "INTEGER NOT NULL DEFAULT 1",
    "venda_cliente_id": "INTEGER NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

VendasItem = Table("vendas_item", vendas_item_columns)
