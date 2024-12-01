async function salvarPagamento() {
  saveForm("#modal-pagamento form", "/pagamentos/");
}

async function editarPagamento(pagamentoID) {
  editForm(pagamentoID, "#modal-pagamento", "/pagamentos/");
}

function deletePagamento(pagamentoID) {
  deleteForm(pagamentoID, "/pagamentos/");
}
