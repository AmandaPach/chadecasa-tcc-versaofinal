async function salvarTipoProduto() {
  saveForm(
    "#modal-tipo-produto form",
    "/produtos/tipos/"
  );
}

async function editarTipoProduto(tipoProdutoID) {
  editForm(
    tipoProdutoID,
    "#modal-tipo-produto",
    "/produtos/tipos/"
  );
}

function deleteTipoProduto(tipoProdutoID) {
  deleteForm(
    tipoProdutoID,
    "/produtos/tipos/"
  );
}
