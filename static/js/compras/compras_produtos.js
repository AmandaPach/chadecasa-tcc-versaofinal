const totalDisplay = document.getElementById("total_produtos");
const totalInput = document.getElementById("valor_total");

const updateTotalValue = () => {
  let formset = document.querySelectorAll("#formset-items-produtos tbody tr");
  var total = 0;
  formset.forEach(form => {
    var quantidade = form.querySelector("input[name$=quantidade]").value;
    var custo = form.querySelector("input[name$=custo]").value;
    var desconto = form.querySelector("input[name$=desconto]").value ?? 0;
    var unidadeDisplay = form.querySelector("input[name$=unidadeCusto]");
    quantidade = parseInt(quantidade);
    custo = parseFloat(custo.replace("R$ ", "").replace(",", "."));
    desconto = parseFloat(desconto.replace("R$ ", "").replace(",", "."));
    const unidadeCusto = quantidade * (custo - desconto);
    unidadeDisplay.value = unidadeCusto.toFixed(2);
    total += unidadeCusto;
  });
  totalDisplay.innerText = total.toFixed(2);
  totalInput.value = total.toFixed(2);
  const totalAll = total + pegarOutrosValores();
  document.querySelector("#total").innerText = totalAll.toFixed(2);
};

function removeItem(btn) {
  btn.closest("tr").remove();
  const formset = document.querySelectorAll("#formset-items-produtos tbody tr");
  if (formset.length == 0) addProdutoInput();
  updateTotalValue();
}

async function getProdutoList(compra=null, venda=null) {
  const response = await fetch("/produtos/options?compra=true");
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
  newForm.querySelector("button").classList.add("itens-compra");
  
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

const checkVendavel = async (produtoField) => {
  const produtoID = produtoField.value;
  const response = await fetch(`/produtos/${produtoID}/`);
  const responseData = await response.json();
  const vendavel = responseData.vendavel == "True";
  const parentRow = produtoField.parentElement.parentElement;
  const custoField = parentRow.querySelector("[name='custo']");
  custoField.value = vendavel ? responseData['preco_custo_produto'] : 0;
}


function verifyProduto(elem) {
  if (elem.value === "new") return abrirModal("#modal-produto");
  updateTotal();
  checkVendavel(elem);
}

const convertDate = (dateStr) => {
  const [year, month, day] = dateStr.split("-");
  return new Date(year, month - 1, day);
}

const dateToStr = (date) => {
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  return `${year}-${month}-${day}`;
}

const today = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Sao_Paulo" }));
const formattedToday = today.toISOString().split("T")[0];

function verifyDates() {
  const dataEmissaoComp = document.getElementById("data_emissao");
  const dataChegadaComp = document.getElementById("data_chegada");

  const dataEmissaoValue = convertDate(dataEmissaoComp.value);
  const dataChegadaValue = convertDate(dataChegadaComp.value);

  const today = new Date();
  const formattedToday = today.toISOString().split('T')[0]; 

  if (dataEmissaoValue > today) {
    dataEmissaoComp.value = formattedToday;
  }

  const dataChegadaYear = dataChegadaValue.getFullYear();
  if (dataChegadaYear < 1000) return;

  if (!dataEmissaoValue || !dataChegadaValue) return;

  if (dataChegadaValue < dataEmissaoValue) {
    dataChegadaComp.value = dateToStr(dataEmissaoValue);
  }
}