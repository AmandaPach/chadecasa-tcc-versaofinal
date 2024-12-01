const fornecedorPath = "/fornecedores/";

async function salvarFornecedor() {
  saveForm("#modal-fornecedor form", fornecedorPath);
}

async function editarFornecedor(fornecedorID) {
  editForm(fornecedorID, "#modal-fornecedor", fornecedorPath);
}

function deleteFornecedor(fornecedorID) {
  deleteForm(fornecedorID, fornecedorPath);
}

async function salvarCidade() {
  salvarCidadeGeneric("#modal-fornecedor", "#cidade_id");
}
