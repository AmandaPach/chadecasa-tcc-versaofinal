async function salvarProduto() {
  const fields = document.querySelectorAll("#modal-produto *:not(.edit-field) :is(select, input:not(#preco_venda_produto))");
  fields.forEach(field => {
    field.removeAttribute("readonly");
    field.removeAttribute("disabled");
  });
  saveForm("#modal-produto form", "/produtos/");
}

async function editarProduto(produtoID) {
  const produtoContent = editForm(produtoID, "#modal-produto", "/produtos/");
  if (!produtoContent) return;
  const { vendavel, compravel, bloqueado } = await produtoContent;

  const fields = document.querySelectorAll("#modal-produto *:not(.edit-field) :is(select, input:not(#preco_venda_produto))");
  if (bloqueado) {
    fields.forEach(field => {
      field.setAttribute("readonly", true);
      field.setAttribute("disabled", true);
    });
  } else {
    fields.forEach(field => {
      field.removeAttribute("readonly");
      field.removeAttribute("disabled");
    });
  }

  const somenteVendavel = vendavel === "True" && compravel !== "True";
  if (somenteVendavel)
    return document.querySelector("#quantidade").removeAttribute("readonly");
  document.querySelector("#quantidade").setAttribute("readonly", true);
}

function deleteProduto(produtoID) {
  deleteForm(produtoID, "/produtos/");
}

async function salvarTipoProduto() {
  saveForm(
    "#modal-tipo-produto form",
    "/produtos/tipos/",
    (nextModalSelector = "#modal-produto"),
    (fieldSelector = "#tipo_id")
  );
}

async function salvarCategoria() {
  saveForm(
    "#modal-categoria form",
    "/produtos/categorias/",
    (nextModalSelector = "#modal-produto"),
    (fieldSelector = "#categoria_id")
  );
}

const categoriaSelect = document.querySelector("#categoria_id");
categoriaSelect.addEventListener("change", (e) => {
  if (e.target.value != "new") return;
  abrirModal("#modal-categoria");
  categoriaSelect.value = "";
});
