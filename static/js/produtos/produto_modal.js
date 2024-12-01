const lockPricesFields = () => {
  const priceFields = document.querySelectorAll('.price_field');
  priceFields.forEach(field => field.setAttribute('readonly', true));
}

const unlockPricesFields = () => {
  const priceFields = document.querySelectorAll('.price_field');
  priceFields.forEach(field => field.disabled = false);
}

const isVendavel = async (tipoProdutoID) => {
  const response = await fetch(`/produtos/tipos/${tipoProdutoID}/`);
  const responseData = await response.json();
  return responseData.vendavel == "True";
}

const tipoSelect = document.querySelector('#tipo_id');
tipoSelect.addEventListener('change', async (e) => {
  const {value} = e.target;
  if (value === "new" || !value) return;
  const vendavelReturn = await isVendavel(value) ? unlockPricesFields : lockPricesFields;
  return vendavelReturn();
});

const tipoProdSelect = document.querySelector("#tipo_id");
tipoProdSelect.addEventListener("change", async e => {
  const {value} = e.target;
  if (value === "new") return abrirModal("#modal-tipo-produto");
  if (!value) return;

  const custo = document.querySelector("#preco_custo_produto");
  const venda = document.querySelector("#preco_venda_produto");
  const response = await fetch(`/produtos/tipos/${value}`);
  const responseData = await response.json();
  const compravel = responseData.compravel === "True";
  const vendavel = responseData.vendavel === "True";
  custo.disabled = false;
  venda.disabled = false;
  const quantidadeComp = document.querySelector("#quantidade");
  if (vendavel && !compravel) {
    custo.removeAttribute("readonly");
    venda.removeAttribute("readonly");
    quantidadeComp.removeAttribute("readonly");
    return;
  }

  quantidadeComp.setAttribute("readonly", true);

  if (vendavel && compravel) {
    custo.setAttribute("readonly", true);
    venda.removeAttribute("readonly");
    return;
  }

  if (!vendavel && compravel) {
    custo.removeAttribute("readonly");
    venda.setAttribute("readonly", true);
    return;
  }
});
