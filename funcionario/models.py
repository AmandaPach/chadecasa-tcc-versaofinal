from database.db import Table


funcionario_columns = {
    "nome_funcionario": "VARCHAR(100) NOT NULL",
    "sobrenome_funcionario": "VARCHAR(100) NOT NULL",
    "sexo_funcionario": "CHAR(5) NOT NULL",
    "telefone_funcionario": "VARCHAR(15) NOT NULL",
    "data_nascimento_funcionario": "DATE NOT NULL",
    "estrangeiro_funcionario": "BOOLEAN",
    "cpf_funcionario": "VARCHAR(14)",
    "rg_funcionario": "VARCHAR(20)",
    "cargo_id": "INTEGER",
    "cidade_id": "INTEGER",
    "rua_funcionario": "VARCHAR(100) NOT NULL",
    "cep_funcionario": "VARCHAR(10) NOT NULL",
    "bairro_funcionario": "VARCHAR(40) NOT NULL",
    "numero_rua_funcionario": "VARCHAR(10) NOT NULL",
    "complemento_funcionario": "VARCHAR(100)",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}


def transform_data_funcionario(data):
    data["nome_funcionario"] = data["nome_funcionario"].upper()
    data["sobrenome_funcionario"] = data["sobrenome_funcionario"].upper()
    return data


Funcionario = Table(
    "Funcionario", funcionario_columns, transform_data=transform_data_funcionario
)


cargo_columns = {
    "nome_cargo": "VARCHAR(40) NOT NULL",
    "descricao_cargo": "VARCHAR(100)",
    "salario_base_cargo": "DECIMAL(10,2) NOT NULL",
    "data_cadastro": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "data_ultima_alteracao": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
}


Cargo = Table("Cargo", cargo_columns)
