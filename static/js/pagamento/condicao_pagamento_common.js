const verifyPercent = () => {
  const percentualInputs = document.querySelectorAll(
    "input[name='percentual']"
  );
  const percentualAlert = document.querySelector("#percentual__alert");
  let total = 0;

  percentualInputs.forEach((input) => {
    total += parseFloat(input.value);
  });

  percentualAlert.style.display = total === 100 ? "none" : "block";
};

const removerLinha = (button) => {
  const row = button.closest("tr");
  row.remove();
};

async function getPagamentoOptions() {
  const response = await fetch("/pagamentos/options/");
  const parcelas = await response.json();
  const parcelasOptions = parcelas.map(({ id: parcelaId, nome }) => {
    const option = document.createElement("option");
    option.value = parcelaId;
    option.textContent = parcelaId + " - " + nome;
    return option;
  });

  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.textContent = "Selecione a forma de pagamento";
  emptyOption.selected = true;

  const createOption = document.createElement("option");
  createOption.value = "new";
  createOption.textContent = "Nova forma de pagamento";

  return [createOption, emptyOption, ...parcelasOptions];
}

const addParcelaInput = () => {
  const newFormHtml = document.querySelector("#empty-form-parcela").innerHTML;
  const newForm = document.createElement("tr");
  newForm.innerHTML = newFormHtml;
  newForm
    .querySelector("input[name='percentual']")
    .addEventListener("change", verifyPercent);

  const select = newForm.querySelector("select[name='forma_pagamento']");
  getPagamentoOptions().then((options) => {
    options.forEach((option) => select.appendChild(option));
  });
  select.addEventListener("change", () => {
    if (select.value !== "new") return;
    abrirModal("#modal-pagamento");
    select.value = "";
  });

  newForm.querySelector("input[name='parcela']").value =
    document.querySelectorAll("#formset-items-parcelas tbody tr").length + 1;

  const tbody = document.querySelector("#formset-items-parcelas tbody");
  tbody.appendChild(newForm);

  setFields();
};

addParcelaInput();
