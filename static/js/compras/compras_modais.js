async function salvarProduto() {
  await saveForm(
    "#modal-produto form",
    "/produtos/",
    (nextModalSelector = "#modal-compras"),
    (fieldSelector = "[name='produto_id']")
  );
}

async function salvarTipoProduto() {
  saveForm(
    "#modal-tipo-produto form",
    "/produtos/tipos/",
    (nextModalSelector = "#modal-produto"),
    (fieldSelector = "#tipo_id")
  );
}

const tipoProdutoSelect = document.querySelector("#tipo_id");
tipoProdutoSelect.addEventListener("change", () => {
  if (tipoProdutoSelect.value !== "new") return;
  abrirModal("#modal-tipo-produto");
  tipoProdutoSelect.value = "";
});

async function salvarCategoria() {
  saveForm(
    "#modal-categoria form",
    "/produtos/categorias/",
    (nextModalSelector = "#modal-produto"),
    (fieldSelector = "#categoria_id")
  );
}

const categoriaSelect = document.querySelector("#categoria_id");
categoriaSelect.addEventListener("change", () => {
  if (categoriaSelect.value !== "new") return;
  abrirModal("#modal-categoria");
  categoriaSelect.value = "";
});

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
    (nextModalSelector = "#modal-compras"),
    (fieldSelector = "#condicao_pagamento_id")
  );
  pegarParcelas();
}

const condicaoSelect = document.querySelector("#condicao_pagamento_id");
condicaoSelect.addEventListener("change", () => {
  if (condicaoSelect.value !== "new") return;
  abrirModal("#modal-condicao");
  condicaoSelect.value = "";
});

async function salvarPagamento() {
  saveForm(
    "#modal-pagamento form",
    "/pagamentos/",
    (nextModalSelector = "#modal-condicao"),
    (fieldSelector = "[name='forma_pagamento']")
  );
}

const formaPagamentoSelect = document.querySelector("[name='forma_pagamento']");
formaPagamentoSelect.addEventListener("change", () => {
  if (formaPagamentoSelect.value !== "new") return;
  abrirModal("#modal-pagamento");
  formaPagamentoSelect.value = "";
});

async function salvarFornecedor() {
  saveForm(
    "#modal-fornecedor form",
    "/fornecedores/",
    (nextModalSelector = "#modal-compras"),
    (fieldSelector = "#fornecedor_id")
  );
}

async function salvarCidade() {
  salvarCidadeGeneric("#modal-fornecedor", "#cidade_id");
}


async function salvarNotaFiscal() {
  saveForm(
    "#modal-nota-fiscal form",
    "/pagamentos/nota_fiscal/",
    (nextModalSelector = "#modal-compras"),
    (fieldSelector = "#nota_fiscal_id")
  );
}

const clienteSelect = document.querySelector("#cliente_id");
if (clienteSelect) {
  clienteSelect.addEventListener("change", () => {
    if (clienteSelect.value !== "new") return;
    abrirModal("#modal-cliente");
    clienteSelect.value = "";
  });
}

const fornecedorSelect = document.querySelector("#fornecedor_id");
if (fornecedorSelect) {
  fornecedorSelect.addEventListener("change", () => {
    if (fornecedorSelect.value !== "new") return;
    abrirModal("#modal-fornecedor");
    fornecedorSelect.value = "";
  });
}