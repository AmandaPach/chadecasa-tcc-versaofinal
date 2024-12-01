async function salvarCidadeGeneric(nextModalSelector=null, fieldSelector=null) {
  saveForm(
    "#modal-cidade form",
    "/local/cidades/",
    nextModalSelector,
    fieldSelector
  );
}

async function salvarEstado() {
  const {id, nome} = saveForm(
    "#modal-estado form",
    "/local/estados/",
    (nextModalSelector = "#modal-cidade"),
    (fieldSelector = "#estado_id")
  );

  
}

async function salvarPais() {
  saveForm(
    "#modal-pais form",
    "/local/paises/",
    (nextModalSelector = "#modal-estado"),
    (fieldSelector = "#pais_id")
  );
}

const cidadeSelectComp = document.querySelector("#cidade_id");
if (cidadeSelectComp) {
  cidadeSelectComp.addEventListener("change", (e) => {
    if (e.target.value !== "new") return;
    abrirModal("#modal-cidade");
    cidadeSelectComp.value = "";
  });
}

const estadoSelectComps = document.querySelectorAll("#estado_id");
estadoSelectComps.forEach(estadoSelect => {
  estadoSelect.addEventListener("change", () => {
    if (estadoSelect.value !== "new") return;
    abrirModal("#modal-estado");
    estadoSelect.value = "";
  });
});

const paisSelect = document.querySelector("#pais_id");
paisSelect.addEventListener("change", (e) => {
  if (e.target.value !== "new") return;
  abrirModal("#modal-pais");
  paisSelect.value = "";
});