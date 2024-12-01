from database.db import Table

cliente_columns = {
    "nome_cliente": "VARCHAR(40) NOT NULL",
    "sobrenome_cliente": "VARCHAR(100) NOT NULL",
    "sexo_cliente": "CHAR(5) NOT NULL",
    "telefone_cliente": "VARCHAR(15) NOT NULL",
    "data_nascimento_cliente": "DATE NOT NULL",
    "cpf_cliente": "VARCHAR(14)",
    "rg_cliente": "VARCHAR(20)",
    "rua_cliente": "VARCHAR(100) NOT NULL",
    "cep_cliente": "VARCHAR(10) NOT NULL",
    "bairro_cliente": "VARCHAR(40) NOT NULL",
    "numero_rua_cliente": "VARCHAR(10) NOT NULL",
    "complemento_cliente": "VARCHAR(100)",
    "estrangeiro_cliente": "BOOLEAN NOT NULL DEFAULT FALSE",
    "cidade_id": "INTEGER",
    "estado_id": "INTEGER",
    "status": "BOOLEAN NOT NULL DEFAULT TRUE",
    "apagado": "BOOLEAN NOT NULL DEFAULT FALSE",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}


def transform_data(data):
    uppercase_fields = [
        "nome_cliente",
        "sobrenome_cliente",
        "rua_cliente",
        "bairro_cliente",
    ]
    for field in uppercase_fields:
        data[field] = data[field].upper()
    if data["complemento_cliente"]:
        data["complemento_cliente"] = data["complemento_cliente"].upper()

    return data


Cliente = Table("Cliente", cliente_columns, transform_data=transform_data)
