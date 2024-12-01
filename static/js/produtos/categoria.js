async function salvarCategoria() {
  saveForm("#modal-categoria form", "/produtos/categorias/");
}

async function editarCategoria(categoriaID) {
  editForm(categoriaID, "#modal-categoria", "/produtos/categorias/");
}

function deleteCategoria(categoriaID) {
  deleteForm(categoriaID, "/produtos/categorias/");
}