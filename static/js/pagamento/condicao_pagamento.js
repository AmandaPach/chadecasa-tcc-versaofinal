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
  saveForm("#modal-condicao form", "/pagamentos/condicao/");
}

async function editarCondicao(condicaoID) {
  const { parcelas } = await editForm(condicaoID, "#modal-condicao", "/pagamentos/condicao/");
  if (!parcelas) return;
  document.querySelector("#formset-items-parcelas tbody").innerHTML = "";
  parcelas.forEach( parcela => {
    let porcentagem = parcela.porcentagem_pgto_parcela;
    porcentagem = `${porcentagem}`.replace("%", "");
    porcentagem = parseFloat(porcentagem).toFixed(2);
    
    addParcelaInput();
    const lastRow = document.querySelector(
      "#formset-items-parcelas tbody tr:last-child"
    );
    lastRow.querySelector("input[name='parcela']").value = parcela.numero_parcela;
    lastRow.querySelector("input[name='percentual']").value = porcentagem;
    lastRow.querySelector("input[name='dias']").value = parcela.dia_pgto_parcela;
    lastRow.querySelector("input[name='taxa']").value = parcela.juros_pgto_parcela;
    lastRow.querySelector("input[name='multa']").value = parcela.multa_pgto_parcela;
    lastRow.querySelector("input[name='desconto']").value = parcela.desconto_pgto_parcela;
    lastRow.querySelector("select[name='forma_pagamento']").value = parcela.forma_pagamento;
  })
} 

function deleteCondicao(condicaoID) {
  deleteForm(condicaoID, "/pagamentos/condicao/");
}

async function abrirModalParcelas(condicaoID) {
  if (!condicaoID || condicaoID == "new") return;
  const response = await fetch(`/pagamentos/condicao/${condicaoID}/`);

  if (!response.ok) {
    alert("Erro ao buscar parcelas da condição de pagamento");
    return;
  }

  abrirModal("#modal-condicao-parcelas");
  const { parcelas } = await response.json();
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
    `;
    document.querySelector("#modal-condicao-parcelas tbody").appendChild(tr);
  })

  if (parcelas.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = "<td class='text-center' colspan='7'>Nenhuma parcela encontrada</td>";
    document.querySelector("#modal-condicao-parcelas tbody").appendChild(tr);
  }
}

function fecharModalParcelas() {
  document.querySelector("#modal-condicao-parcelas table tbody").innerHTML = "";
  fecharModal('#modal-condicao-parcelas');
}


const formaPagamentoSelect = document.querySelector("[name='forma_pagamento']");
formaPagamentoSelect.addEventListener('change', () => {
  if (formaPagamentoSelect.value !== 'new') return;
  abrirModal('#modal-pagamento');
  formaPagamentoSelect.value = '';
});

const salvarPagamento = () => saveForm(
  "#modal-pagamento form",
  "/pagamentos/",
  (nextModalSelector = "#modal-condicao"),
  (fieldSelector = "[name='forma_pagamento']")
);