const cidadePath = "/local/cidades/";

async function salvarCidade() {
  saveForm(
    "#modal-cidade form",
    cidadePath
  );
}

async function editarCidade(cidadeID) {
  editForm(
    cidadeID,
    "#modal-cidade",
    cidadePath
  );
}

function deleteCidade(cidadeID) {
  deleteForm(
    cidadeID,
    cidadePath
  );
}
