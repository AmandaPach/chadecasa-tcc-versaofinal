from database.db import Table

compras_columns = {
    "nota_fiscal": "INTEGER NOT NULL",
    "modelo_id": "INTEGER NOT NULL",
    "serie": "INTEGER NOT NULL DEFAULT 1",
    "fornecedor_id": "INTEGER NOT NULL",
    "condicao_pagamento_id": "INTEGER NOT NULL",
    "frete": "INTEGER NOT NULL DEFAULT 0",
    "seguro": "INTEGER NOT NULL DEFAULT 0",
    "outras_despesas": "INTEGER NOT NULL DEFAULT 0",
    "valor_total": "INTEGER NOT NULL",
    "data_chegada": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_emissao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "cancelado": "BOOLEAN NOT NULL DEFAULT FALSE",
}

Compras = Table(
    "compras", compras_columns, primary_keys=["nota_fiscal", "modelo_id", "serie", "fornecedor_id"]
)

compras_item_columns = {
    "quantidade": "INTEGER NOT NULL",
    "custo": "INTEGER NOT NULL",
    "desconto": "INTEGER NOT NULL",
    "produto_id": "INTEGER NOT NULL",
    "compra_nota_fiscal": "INTEGER NOT NULL",
    "compra_modelo_id": "INTEGER NOT NULL DEFAULT 55",
    "compra_serie": "INTEGER NOT NULL DEFAULT 1",
    "compra_fornecedor_id": "INTEGER NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

ComprasItem = Table("compras_item", compras_item_columns)
