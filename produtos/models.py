from database.db import Table

produto_columns = {
    "nome_produto": "VARCHAR(20) NOT NULL UNIQUE",
    "descricao_produto": "TEXT",
    "preco_custo_produto": "DECIMAL(10,2) NOT NULL",
    "preco_venda_produto": "DECIMAL(10,2) NOT NULL",
    "unid_medida_produto": "VARCHAR(5) NOT NULL",
    "quantidade": "INTEGER NOT NULL DEFAULT 0",
    "categoria_id": "INTEGER NOT NULL",
    "tipo_id": "INTEGER NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}
Produto = Table("produto", produto_columns)

categoria_columns = {
    "nome_categoria": "VARCHAR(100) NOT NULL UNIQUE",
    "descricao_categoria": "TEXT",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

Categoria = Table("categoria", categoria_columns)

tipo_produto_columns = {
    "nome_tipo": "VARCHAR(20) NOT NULL UNIQUE",
    "descricao_tipo": "TEXT",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "vendavel": "BOOLEAN NOT NULL DEFAULT TRUE",
    "compravel": "BOOLEAN NOT NULL DEFAULT TRUE",
}

TipoProduto = Table("tipo_produto", tipo_produto_columns)
