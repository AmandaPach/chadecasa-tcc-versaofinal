const clientePath = "/clientes/";

async function salvarCliente() {
  saveForm("#modal-cliente form", clientePath);
}

async function editarCliente(clienteID) {
  editForm(clienteID, "#modal-cliente", clientePath);
}

function deleteCliente(clienteID) {
  deleteForm(clienteID, clientePath);
}

async function salvarCidade() {
  salvarCidadeGeneric("#modal-cliente", "#cidade_id");
}

async function limparCliente() {
  const form = document.querySelector("#modal-cliente form");
  const clienteID = form.querySelector("[name='id']").value;
  if (!clienteID) {
    alert("Houve um erro com o cliente.");
    return;
  }
  const response = await fetch(`${clientePath + clienteID}/limpar/`, {
    method: "GET",
  });

  if (response.status === 400) {
    return alert(await response.message);
  }

  window.location.reload();
}
