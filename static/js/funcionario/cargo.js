const cargoPath = "/funcionarios/cargo/";

async function salvarCargo() {
  saveForm(
    "#modal-cargo form",
    cargoPath
  );
}

async function editarCargo(cargoID) {
  editForm(
    cargoID,
    "#modal-cargo",
    cargoPath
  );
}

function deleteCargo(cargoID) {
  deleteForm(
    cargoID,
    cargoPath
  );
}

