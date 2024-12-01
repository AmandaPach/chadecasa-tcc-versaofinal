from database.db import Table

fornecedor_columns = {
    "razao_social_fornecedor": "VARCHAR(250) NOT NULL UNIQUE",
    "nome_fantasia_fornecedor": "VARCHAR(250) NOT NULL UNIQUE",
    "cnpj_fornecedor": "VARCHAR(14) NOT NULL UNIQUE",
    "ie_fornecedor": "VARCHAR(20) NOT NULL UNIQUE",
    "email_fornecedor": "VARCHAR(100) NOT NULL",
    "data_fundacao_fornecedor": "DATE",
    "telefone_fornecedor": "VARCHAR(20) NOT NULL",
    "limite_credito_fornecedor": "DECIMAL(10,2)",
    "rua_fornecedor": "VARCHAR(100) NOT NULL",
    "complemento_fornecedor": "VARCHAR(100)",
    "cep_fornecedor": "VARCHAR(10) NOT NULL",
    "numero_rua_fornecedor": "VARCHAR(10) NOT NULL",
    "bairro_fornecedor": "VARCHAR(100) NOT NULL",
    "cidade_id": "INTEGER",
    "estado_id": "INTEGER",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}


def transform_data(data):
    data["razao_social_fornecedor"] = data["razao_social_fornecedor"].upper()
    data["nome_fantasia_fornecedor"] = data["nome_fantasia_fornecedor"].upper()
    data["rua_fornecedor"] = data["rua_fornecedor"].upper()
    data["bairro_fornecedor"] = data["bairro_fornecedor"].upper()
    data["email_fornecedor"] = data["email_fornecedor"].upper()
    if data["complemento_fornecedor"]:
        data["complemento_fornecedor"] = data["complemento_fornecedor"].upper()
    return data


Fornecedor = Table("fornecedor", fornecedor_columns, transform_data=transform_data)
