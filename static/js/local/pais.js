async function salvarPais() {
  saveForm(
    "#modal-pais form",
    "/local/paises/"
  );
}

async function editarPais(paisID) {
  editForm(
    paisID,
    "#modal-pais",
    "/local/paises/"
  );
}

function deletePais(paisID) {
  deleteForm(
    paisID,
    "/local/paises/"
  );
}