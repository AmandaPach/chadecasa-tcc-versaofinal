const totalDisplay = document.querySelector("#total_produtos");
const totalInput = document.querySelector("#valor_total");

async function salvarVendas() {
  unlockAllFields();
  const form = document.querySelector("#modal-vendas form");
  const formData = new FormData(form);
  const requiredFields = form.querySelectorAll("[required]");
  for (const field of requiredFields) {
    if (!field.value) {
      alert("Preencha todos os campos obrigatórios!");
      return;
    }
  }
  const produtosList = document.querySelectorAll("table tbody tr");
  if (produtosList.length == 0) {
    alert("Adicione pelo menos um produto");
    return;
  }
  
  const response = await fetch("", {
    method: "POST",
    body: formData,
  });
  
  lockAllFields();
  if (response.ok) return window.location.reload();
  
  if (response.status == 400) {
    const responseText = await response.text();
    alert(responseText);
    unlockItensPagamento();
  }
}

const cancelarVenda = async (notaFiscal, modeloNota, serie, clienteID) => {
  const formData = new FormData();
  formData.append("nota_fiscal", notaFiscal);
  formData.append("modelo", modeloNota);
  formData.append("serie", serie);
  formData.append("cliente_id", clienteID);
  const response = await fetch('/vendas/cancelar/', 
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

const updateTotalValue = () => {
  let formset = document.querySelectorAll("#formset-items-produtos tbody tr");
  var total = 0;
  formset.forEach(form => {
    var quantidade = form.querySelector("input[name$=quantidade]").value;
    var custo = form.querySelector("input[name$=custo]").value;
    var desconto = form.querySelector("input[name$=desconto]").value ?? 0;
    var unidadeDisplay = form.querySelector("input[name$=unidadeCusto]");
    custo = parseFloat(custo.replace("R$ ", "").replace(",", "."));
    desconto = parseFloat(desconto.replace("R$ ", "").replace(",", "."));
    const unidadeCusto = quantidade * (custo - desconto);
    unidadeDisplay.value = "R$ " + unidadeCusto.toFixed(2);
    total += unidadeCusto;
  });
  totalDisplay.innerText = total.toFixed(2);
  totalInput.value = total.toFixed(2);
}

function removeItem(btn) {
  btn.closest("tr").remove();
  const formset = document.querySelectorAll("#formset-items-produtos tbody tr");
  if (formset.length == 0) addProdutoInput();
  updateTotalValue();
}

async function getProdutoList() {
  const response = await fetch("/produtos/options?venda=true&quantidade=true");
  const produtos = await response.json();
  const produtosOptions = produtos.map(({id, nome}) => {
    const produtoOption = document.createElement("option");
    produtoOption.value = id;
    produtoOption.innerText = nome;
    return produtoOption;
  })
  
  const emptyOption = document.createElement("option");
  emptyOption.value = "";
  emptyOption.innerText = "Selecione um produto";
  emptyOption.selected = true;

  const createOption = document.createElement("option");
  createOption.value = "new";
  createOption.innerText = "Novo produto";

  return [createOption, emptyOption, ...produtosOptions];
}

function addProdutoInput() {
  const newFormHtml = document.querySelector("#empty-form-produto").innerHTML;
  const newForm = document.createElement("tr");
  newForm.innerHTML = newFormHtml;
  newForm.querySelector("button").classList.add("itens-venda");
  
  const produtoSelect = newForm.querySelector('select');
  getProdutoList().then(options => {
    produtoSelect.innerHTML = "";
    options.forEach(option => produtoSelect.appendChild(option));
  });

  document
    .querySelector("#formset-items-produtos tbody")
    .append(newForm);

  setFields();
}

async function verifyProduto(elem) {
  if (!elem.value) return;
  if (elem.value == "new") return abrirModal("#modal-produto");
  const response = await fetch(`/produtos/${elem.value}`);
  const {preco_venda_produto} = await response.json();
  elem.closest("tr").querySelector("input[name$=custo]").value = preco_venda_produto;
  updateTotal();
}

addProdutoInput();

async function salvarCondicao() {
  const totalPercentInputs = document.querySelectorAll(
    "[name='percentual']"
  );
  let totalPercentValue = 0;
  totalPercentInputs.forEach(input => {
    totalPercentValue += parseFloat(input.value.replace("%", ""));
  })
  if (totalPercentValue != 100) {
    alert("As parcelas devem somar 100%");
    return;
  }
  saveForm(
    "#modal-condicao form",
    "/pagamentos/condicao/",
    (nextModalSelector = "#modal-vendas"),
    (fieldSelector = "#condicao_pagamento_id")
  );
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
  updateTotalValue();
  const totalProdutos = parseFloat(document.querySelector("#total_produtos").innerText);
  const totalOutros = pegarOutrosValores();
  const total = totalProdutos + totalOutros;
  document.querySelector("#total").innerText = total.toFixed(2);
  totalInput.value = total.toFixed(2);
  pegarParcelas();
}

async function pegarParcelas() {
  const condicaoField = document.querySelector("#condicao_pagamento_id");
  if (!condicaoField.value || condicaoField.value == "new") return;

  const { value: condicaoID } = condicaoField;
  const parcelasTable = document.querySelector("#modal-vendas .parcelas tbody");

  const response = await fetch(`/pagamentos/condicao/${condicaoID}`);

  if (!response.ok) {
    alert("Erro ao buscar parcelas da condição de pagamento");
    return;
  }

  const calculaValor = (porcentagem) => {
    const total = parseFloat(document.querySelector("#total").innerText).toFixed(2);
    if (!porcentagem) return total;
    porcentagem = parseFloat(`${porcentagem}`.replace("%", ""));
    const result = (total * porcentagem) / 100;
    return result.toFixed(2);
  }

  const responseData = await response.json();
  console.log(responseData);
  const parcelas = responseData.parcelas;
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
      <td class="percent-item">${parcela.porcentagem_pgto_parcela}</td>
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
  condicaoField.addEventListener("change", () => pegarParcelas());
}

const lockAllFields = () => {
  const formFields = document.querySelectorAll("#modal-vendas .modal-body :is(input, select, button)");
  formFields.forEach(input => {
    input.setAttribute("readonly", true);
    input.setAttribute("disabled", true);
    input.disabled = true;
  });
}

const unlockAllFields = () => {
  const formFields = document.querySelectorAll("#modal-vendas .modal-body :is(input, select, button)");
  formFields.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
    input.disabled = false;
  });
}

const cleanPagamentoFields = () => {
  document.querySelector("#condicao_pagamento_id").value = "";
  document.querySelector(".parcelas tbody").innerHTML = "";
}

const unlockItensVenda = () => {
  lockAllFields();
  const vendaItens = document.querySelectorAll(".itens-venda");
  vendaItens.forEach(input => {
    input.removeAttribute("readonly");
    input.removeAttribute("disabled");
  });
  document.querySelector("#return-produtos").disabled = true;
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

const salvarSecaoProdutos = async () => {
  updateTotal();
  const clienteComponent = document.querySelector("#cliente_id");
  if (!clienteComponent.value || clienteComponent.value == "new") {
    alert("Selecione um cliente");
    return;
  }

  const produtosList = document.querySelectorAll("#formset-items-produtos table tbody tr");
  const produtosForm = []
  produtosList.forEach(row => {
    produto = {
      produto: row.querySelector("select").value,
      quantidade: row.querySelector("input[name$=quantidade]").value,
    }
    if (!produto.produto || !produto.quantidade) return;
    produtosForm.push(produto);
  });
  const formData = new FormData();
  formData.append("produtos", JSON.stringify(produtosForm));
  const response = await fetch("/produtos/check/", {
    method: "POST",
    body: formData,
  })
  if (response.status == 200) {
    mudarSecaoPagamentos();
    return
  }
  const responseText = await response.text();
  alert(responseText);
}

const mudarSecaoProdutos = async () => {
  cleanPagamentoFields();
  unlockItensVenda();
}

function abrirModalVendas() {
  const modalSelector = "#modal-vendas";
  const modalComponent = document.querySelector(modalSelector);
  modalComponent.classList.remove("editing");
  unlockItensVenda();
  abrirModal(modalSelector);
}

function fecharModalVendas() {
  mudarSecaoProdutos();
  fecharModal("#modal-vendas");
  document.querySelector("#modal-vendas form").reset();
  document.querySelector("#formset-items-produtos tbody").innerHTML = "";
  document.querySelector("#modal-vendas .parcelas tbody").innerHTML = "";
  document.querySelectorAll(".itens-compra").forEach((field) => {
    field.disabled = true;
    field.setAttribute("readonly", true);
  });
  document.querySelectorAll(".nota-fiscal").forEach((field) => {
    field.removeAttribute("readonly");
    field.disabled = false;
  });
  addProdutoInput();
  document.querySelector("#save-products").disabled = true;
}

const mudarSecaoPagamentos = async () => {
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
}

async function verVendas(nota_fiscal, modelo, serie, cliente_id) {
  const modalSelector = "#modal-vendas";
  const formData = new FormData();
  formData.append("nota_fiscal", nota_fiscal);
  formData.append("modelo", modelo);
  formData.append("serie", serie);
  formData.append("cliente_id", cliente_id);
  const response = await fetch("/vendas/manage/", {
    method: "POST",
    body: formData,
  });

  if (response.status === 400) {
    const responseMessage = await response.text();
    alert(responseMessage);
    return;
  }

  if (!response.ok) {
    alert("Erro ao buscar dados do servidor");
    return;
  }

  const modalComponent = document.querySelector(modalSelector);
  modalComponent.classList.add("editing");
  
  const contentResponse = await response.json();
  fillForm(contentResponse, modalSelector + " form");
  pegarParcelas();

  $(modalSelector).modal("show");

  const formsetItems = document.querySelector("#formset-items-produtos tbody");
  const vendasItems = contentResponse.itens;

  formsetItems.innerHTML = "";
  let totalProdutos = 0.0;
  vendasItems.forEach( item => {
    const newRow = document.createElement("tr");
    let { produto, quantidade, valor_unitario: custo } = item;
    let totalCusto = parseFloat(custo?.replace("R$", "").replace(",", "."));
    const total = (quantidade * (totalCusto - 0)).toFixed(2);
    totalProdutos += parseFloat(total);
    const fields = ["", produto, quantidade, custo, "R$ 0,00", total, ""];
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
  lockAllFields();
}

updateTotalValue();
mudarSecaoProdutos();