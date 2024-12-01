const modeloPath = "/pagamentos/modelo/";

async function salvarModelo() {
  saveForm("#modal-modelo form", modeloPath);
}

async function editarModelo(modeloID) {
  editForm(modeloID, "#modal-modelo", modeloPath);
}

function deleteModelo(modeloID) {
  deleteForm(modeloID, modeloPath);
}