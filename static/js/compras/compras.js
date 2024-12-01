async function salvarCompras() {
  unlockAllFields();
  const form = document.querySelector("#modal-compras form");
  const formData = new FormData(form);
  const requiredFields = form.querySelectorAll("[required]");
  for (const field of requiredFields) {
    if (!field.value) {
      alert("Preencha todos os campos obrigatórios!");
      return;
    }
  }
  lockAllFields();
  const produtosList = document.querySelectorAll("table tbody tr");
  if (produtosList.length == 0) {
    alert("Adicione pelo menos um produto");
    return;
  }


  const response = await fetch("/compras/", {
    method: "POST",
    body: formData,
  });

  if (response.ok) {
    window.location.reload();
    return;
  }


  if (response.status == 400) {
    const responseText = await response.text();
    alert(responseText);
  }
}

const frete = document.querySelector("#frete");
const seguro = document.querySelector("#seguro");
const outrasDespesas = document.querySelector("#outras_despesas");

frete.addEventListener("input", () => updateTotal());
seguro.addEventListener("input", () => updateTotal());
outrasDespesas.addEventListener("input", () => updateTotal());

function stringToFloat(valor) {
  const numero = valor.replace("R$", "").trim().replace(",", ".");
  const resultado = parseFloat(numero);
  return numero.split(".")[1]?.length === 3 ? resultado * 10 : resultado;
}

const pegarOutrosValores = () => {
  const freteValue = stringToFloat(frete.value);
  const seguroValue = stringToFloat(seguro.value);
  const outrasDespesasValue = stringToFloat(outrasDespesas.value);
  return freteValue + seguroValue + outrasDespesasValue;
}

const updateTotal = () => {
  const totalProdutos = parseFloat(document.querySelector("#total_produtos").innerText);
  const totalOutros = pegarOutrosValores();
  const total = totalProdutos + totalOutros;
  document.querySelector("#valor_total").value = total.toFixed(2);
  document.querySelector("#total").innerText = total.toFixed(2);
  pegarParcelas();
  updateTotalValue();
}

async function pegarParcelas() {
  const condicaoField = document.querySelector("#condicao_pagamento_id");
  if (!condicaoField.value || condicaoField.value == "new") return;

  const { value: condicaoID } = condicaoField;
  const parcelasTable = document.querySelector("#modal-compras .parcelas tbody");

  const response = await fetch(`/pagamentos/condicao/${condicaoID}`);

  if (!response.ok) {
    alert("Erro ao buscar parcelas da condição de pagamento");
    return;
  }

  const calculaValor = (porcentagem) => {
    const total = parseFloat(document.querySelector("#total").innerText);
    if (!porcentagem) return total;
    porcentagem = parseFloat(`${porcentagem}`.replace("%", ""));
    document.querySelector("#valor_total").value = total.toFixed(2);
    const result = (total * porcentagem) / 100;
    return result.toFixed(2);
  }

  const { parcelas } = await response.json();
  if (!parcelas) {
    alert("Houve um erro com a obtenção das parcelas");
    return;
  }
  parcelasTable.innerHTML = "";
  parcelas.forEach(parcela => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${parcela.numero_parcela}</td>
      <td>${parcela.dia_pgto_parcela}</td>
      <td>${parcela.porcentagem_pgto_parcela}</td>
      <td>${parcela.desconto_pgto_parcela}</td>
      <td>${parcela.juros_pgto_parcela}</td>
      <td>${parcela.multa_pgto_parcela}</td>
      <td>${parcela.forma_pagamento}</td>
      <td>${calculaValor(parcela.porcentagem_pgto_parcela)}</td>
    `;
    parcelasTable.appendChild(tr);
  })

  if (parcelas.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = "<td class='text-center' colspan='7'>Nenhuma parcela encontrada</td>";
    parcelasTable.appendChild(tr);
  }
}

const condicaoField = document.querySelector("#condicao_pagamento_id");
if (condicaoField) {
  condicaoField.addEventListener("change", () => pegarParcelas(condicaoField));
}

function fecharModalCompras() {
  fecharModal("#modal-compras");
  document.querySelector("#modal-compras form").reset();
  document.querySelector("#formset-items-produtos tbody").innerHTML = "";
  document.querySelector("#modal-compras .parcelas tbody").innerHTML = "";
  document.querySelectorAll(".itens-compra").forEach((field) => {
    field.disabled = true;
    field.setAttribute("readonly", true);
  });
  document.querySelectorAll(".nota-fiscal").forEach((field) => {
    field.removeAttribute("readonly");
    field.disabled = false;
  });
  document.querySelector("#save-products").disabled = true;
}

function abrirModalCompras() {
  const modalComponent = document.querySelector("#modal-compras");
  modalComponent.classList.remove("editing");
  abrirModal("#modal-compras");
}

async function verCompras(notaFiscal, modelo, serie, fornecedorID) {
  const modalSelector = "#modal-compras";
  const formData = new FormData();
  formData.append("nota_fiscal", notaFiscal);
  formData.append("modelo", modelo);
  formData.append("serie", serie);
  formData.append("fornecedor_id", fornecedorID);
  const response = await fetch(`/compras/manage/`,
    {
      method: 'POST',
      body: formData,
    }
  );

  if (response.status === 400) {
    alert(await response.message);
    return;
  }

  if (!response.ok) {
    alert("Erro ao buscar dados do servidor");
    return;
  }

  const modalComponent = document.querySelector(modalSelector);
  modalComponent.classList.add("editing");

  const contentResponse = await response.json();
  fillForm(contentResponse, `${modalSelector} form`);
  const condicaoField = document.querySelector("#condicao_pagamento_id");
  if (condicaoField) {
    pegarParcelas(condicaoField);
  }

  lockAllFields();
  $(modalSelector).modal("show");

  const comprasItems = contentResponse['itens'];
  const formsetItems = document.querySelector("#formset-items-produtos tbody");
  formsetItems.innerHTML = "";
  let totalProdutos = 0.0;
  comprasItems.forEach(item => {
    const newRow = document.createElement("tr");
    let { produto, quantidade, custo, desconto } = item;
    custo = parseFloat(custo.replace("R$", "").replace(",", "."));
    desconto = parseFloat(desconto.replace("R$", "").replace(",", "."));
    const total = (quantidade * (custo - desconto)).toFixed(2);
    totalProdutos += parseFloat(total);
    const fields = ["", produto, quantidade, custo, desconto, total, ""];
    fields.forEach(value => {
      const newCell = document.createElement("td");
      newCell.innerText = value;
      newRow.appendChild(newCell);
    });
    formsetItems.appendChild(newRow);
    document.querySelector("#total_produtos").innerText = totalProdutos.toFixed(2);
  });

  const totalTodos = totalProdutos + pegarOutrosValores();
  document.querySelector("#total").innerText = totalTodos.toFixed(2);
}

const unlockAllFields = () => {
  const formFields = document.querySelectorAll("#modal-compras .modal-body :is(input, select, button)");
  formFields.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
  });
}

const lockAllFields = () => {
  const formFields = document.querySelectorAll("#modal-compras .modal-body :is(input, select, button)");
  formFields.forEach(input => {
    input.setAttribute("readonly", true);
    input.setAttribute("disabled", true);
    input.disabled = true;
  });
}

const unlockNotaFiscal = () => {
  lockAllFields();
  const notaFiscalInputs = document.querySelectorAll(".nota-fiscal");
  notaFiscalInputs.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
  });
}

const unlockItensCompra = () => {
  lockAllFields();
  const itensCompra = document.querySelectorAll(".itens-compra");
  itensCompra.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
  });
  document.querySelector("#return-nota").disabled = false;
}

const unlockItensPagamento = () => {
  lockAllFields();
  const pagamentoItens = document.querySelectorAll(".itens-pagamento");
  pagamentoItens.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
  });
  document.querySelector("#return-produtos").disabled = false;
}

const cancelarCompra = async (notaFiscal, modeloNota, serie, fornecedorID) => {
  const formData = new FormData();
  formData.append("nota_fiscal", notaFiscal);
  formData.append("modelo", modeloNota);
  formData.append("serie", serie);
  formData.append("fornecedor_id", fornecedorID);
  const response = await fetch('/compras/cancelar/', 
    {
      method: 'POST',
      body: formData
    }
  );

  if (response.ok) {
    window.location.reload();
    return;
  }

  alert("Erro ao cancelar compra");
}

unlockNotaFiscal();

const mudarSecaoProdutos = async () => {
  const produtosList = document.querySelectorAll("#formset-items-produtos [required]");
  let continueLoop = true;
  produtosList.forEach( produto => {
    if (!continueLoop) return;
    if (produto.value == "new" || produto.value == "") {
      continueLoop = false;
      return;
    }
  })
  if (!continueLoop) {
    alert("Preencha todos os campos obrigatórios");
    return;
  };
  unlockItensPagamento();
  updateTotal();
}
