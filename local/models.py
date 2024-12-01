from database.db import Table

pais_columns = {
    "nome_pais": "VARCHAR(100) NOT NULL UNIQUE",
    "sigla_pais": "VARCHAR(3)",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "atual": "BOOLEAN NOT NULL DEFAULT FALSE",
}

Pais = Table("Pais", pais_columns)

estado_columns = {
    "nome_estado": "VARCHAR(100) NOT NULL UNIQUE",
    "sigla_estado": "VARCHAR(3)",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "pais_id": "INT NOT NULL",
}

Estado = Table("Estado", estado_columns)

cidade_columns = {
    "nome_cidade": "VARCHAR(100) NOT NULL",
    "ddd_cidade": "VARCHAR(3) NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "estado_id": "INT NOT NULL",
}

Cidade = Table("Cidade", cidade_columns)
