function verifyNotaFiscal() {
  const notaFiscal = document.getElementById("nota_fiscal");
  const modelo = document.getElementById("modelo_id");
  const serie = document.getElementById("serie");
  const fornecedor = document.getElementById("fornecedor_id");
  const notaFiscalInputs = [notaFiscal, modelo, serie, fornecedor];

  if (!notaFiscal.value || !modelo.value || !serie.value || !fornecedor.value) {
    alert("Preencha todos os campos obrigatórios.");
    return;
  };

  const formData = new FormData();
  formData.append("nota_fiscal", notaFiscal.value);
  formData.append("modelo", modelo.value);
  formData.append("serie", serie.value);
  formData.append("fornecedor", fornecedor.value);

  fetch('/compras/nota/', {
    method: 'POST',
    body: formData,
  }).then(response => {
    if (response.status !== 200) {
      notaFiscalInputs.forEach(input => input.value = "");
      return alert("Nota fiscal já cadastrada para esse fornecedor.");
    }
    notaFiscalInputs.forEach(input => {
      input.setAttribute("readonly", true);
    });
    unlockItensCompra();
    addProdutoInput();
    document.querySelector("#verify-nota").disabled = true;
    return;
  });
}