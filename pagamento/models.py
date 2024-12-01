from django.db import models
from django.utils import timezone
from database.db import Table

pagamento_columns = {
    "nome_pagamento": "VARCHAR(100) NOT NULL UNIQUE",
    "descricao_pagamento": "VARCHAR(255)",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

Pagamento = Table("Pagamento", pagamento_columns)

condicao_pagamento_columns = {
    "nome_condicao_pgto": "VARCHAR(20) NOT NULL UNIQUE",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "parcela": "INT NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

CondicaoPagamento = Table("CondicaoPagamento", condicao_pagamento_columns)

parcela_columns = {
    "numero_parcela": "INT NOT NULL",
    "dia_pgto_parcela": "INT NOT NULL",
    "porcentagem_pgto_parcela": "DECIMAL(5,2) NOT NULL",
    "desconto_pgto_parcela": "DECIMAL(5,2) NOT NULL DEFAULT 0",
    "juros_pgto_parcela": "DECIMAL(5,2) NOT NULL DEFAULT 0",
    "multa_pgto_parcela": "DECIMAL(5,2) NOT NULL DEFAULT 0",
    "forma_pgto_id": "INT NOT NULL",
    "condicao_pgto_id": "INT NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

Parcela = Table("Parcela", parcela_columns)

modelo_columns = {
    "numero_modelo": "VARCHAR(20) NOT NULL",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "descricao_modelo": "VARCHAR(255)",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}

Modelo = Table("Modelo", modelo_columns)