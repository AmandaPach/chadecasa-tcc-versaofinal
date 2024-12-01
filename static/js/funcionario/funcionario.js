const cargoSelect = document.querySelector("#cargo_id");
const funcionarioPath = "/funcionarios/";

async function salvarFuncionario() {
  saveForm("#modal-funcionario form", funcionarioPath);
}

async function editarFuncionario(funcionarioID) {
  editForm(funcionarioID, "#modal-funcionario", funcionarioPath);
}

function deleteFuncionario(funcionarioID) {
  deleteForm(funcionarioID, funcionarioPath);
}

async function salvarCargo() {
  saveForm(
    "#modal-cargo form",
    "/funcionarios/cargo/",
    (nextModalSelector = "#modal-funcionario"),
    (fieldSelector = "#cargo_id")
  );
}

async function salvarCidade() {
  salvarCidadeGeneric("#modal-funcionario", "#cidade_id");
}

cargoSelect.addEventListener("change", e => {
  if (e.target.value !== "new") return;
  abrirModal("#modal-cargo");
  cargoSelect.value = "";
});