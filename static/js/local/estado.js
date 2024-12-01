const paisSelect = document.querySelector("#pais_id");
const estadoPath = "/local/estados/";

async function salvarEstado() {
  saveForm(
    "#modal-estado form",
    estadoPath
  );
}

async function editarEstado(estadoID) {
  editForm(
    estadoID,
    "#modal-estado",
    estadoPath
  );
}

function deleteEstado(estadoID) {
  deleteForm(
    estadoID,
    estadoPath
  );
}

async function salvarPais() {
  saveForm(
    "#modal-pais form",
    "/local/paises/",
    "#modal-estado",
    "#pais_id"
  );
}

paisSelect.addEventListener("change", (event) => {
  if (event.target.value === "new") {
    abrirModal("#modal-pais");
  }
});
