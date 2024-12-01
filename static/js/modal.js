function abrirModal(modalSelector, cleanForms=false) {
  fecharTodasModais(cleanForms);
  $(modalSelector).modal("show");
}

function fecharModal(modalSelector, cleanForms=true) {
  const modal = document.querySelector(modalSelector);
  modal.querySelectorAll("select[value='new']").forEach((select) => {
    select.value = "";
  });
  const form = modal.querySelector("form");
  if (form) form.classList.remove("editing");
  if (form && cleanForms) form.reset();
  const idInput = modal.querySelector("[name='id']");
  if (idInput) idInput.value = "";
  $(modalSelector).modal("hide");
  const parcelasTable = modal.querySelector(".parcelas table tbody");
  if (parcelasTable) parcelasTable.innerHTML = "";
}

function fecharTodasModais(cleanForms=true) {
  const openModais = document.querySelectorAll(".modal.show");
  openModais.forEach( modal => fecharModal(`#${modal.id}`, cleanForms));
}
