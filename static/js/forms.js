const formatDate = (dateStr) => {
  if (!dateStr) return "";
  const [date, ...rest] = dateStr.split(" ");
  const [year, month, day] = date.split("-");
  return `${day}/${month}/${year}`;
}

function fillForm(contentResponse, formSelector) {
  const form = document.querySelector(formSelector);
  Object.keys(contentResponse).forEach(key => {
    let input = form.querySelector(`#${key}`);
    if (!input) {
      console.log(`Campo ${key} não encontrado`);
      return;
    }

    if (input.type == "checkbox") {
      input.checked = contentResponse[key] != 'False';
      return;
    }

    if (input.type == "date") {
      const filteredDate = contentResponse[key].split(" ")[0];
      input.value = filteredDate;
      return;
    }

    const dateFields = ["data_cadastro", "data_ultima_alteracao"];
    if (dateFields.includes(key)) {
      input.value = formatDate(contentResponse[key]);
      return;
    }

    input.value = contentResponse[key];
  });

  const createdAtField = document.querySelector("#created_at");
  const createdAtValue = formatDate(contentResponse["data_ultima_alteracao"]);
  if (createdAtField) createdAtField.textContent = createdAtValue;
}

async function saveForm(formSelector, url, nextModalSelector=null, fieldSelector=null) {
  const form = document.querySelector(formSelector);
  const requiredFields = form.querySelectorAll("[required]:not(.edit-field)");

  let shouldContinue = true;

  requiredFields.forEach(field => {
    if (!field.value) {
      alert("Preencha todos os campos obrigatórios!");
      shouldContinue = false;
      return;
    }

    const label = form.querySelector(`label[for="${field.id}"]`)?.textContent ?? "Campo";
    const minlength = field.getAttribute("minlength");
    const maxlength = field.getAttribute("maxlength");
    if (!minlength) field.setAttribute("minlength", 1);
    if (field.value.length < minlength) {
      alert(`O campo ${label} não tem o tamanho mínimo: ${minlength} caracteres`);
      shouldContinue = false;
      return;
    }

    if (maxlength && field.value.length > maxlength) {
      alert(`O campo ${label} superou o tamanho máximo: ${maxlength} caracteres`);
      shouldContinue = false;
      return;
    }
  });

  if (!shouldContinue) return;

  const formData = new FormData(form);
  formResponse = await fetch(url, {
    method: "POST",
    body: formData,
  });
  
  if (formResponse.status === 400) {
    alert(await formResponse.text());
    return;
  }

  if (!nextModalSelector) window.location.reload();

  const { id: responseID, nome: responseNome} = await formResponse.json();

  abrirModal(nextModalSelector, true);
  const selectComponents = document.querySelectorAll(fieldSelector);
  selectComponents.forEach(select => {
    const option = document.createElement("option");
    option.textContent = responseNome;
    option.value = responseID;
    select.appendChild(option);
    if (select.value == "new" || !select.value)
      select.value = responseID;
  })
  return { id: responseID, nome: responseNome };
}

async function editForm(contentID, modalSelector, url) {
  const response = await fetch(`${url}${contentID}/`);

  if (!response.ok) {
    alert("Erro ao buscar dados do servidor");
    return;
  }

  const modalComponent = document.querySelector(modalSelector);
  modalComponent.classList.add("editing");

  const contentResponse = await response.json();
  fillForm(contentResponse, `${modalSelector} form`);

  $(modalSelector).modal("show");
  return contentResponse;
}

async function deleteForm(contentID, url) {
  if (!confirm("Deseja realmente excluir este registro?")) return;
  const response = await fetch(`${url}${contentID}/`, { method: "DELETE" });

  if (response.status === 400) {
    return alert(await response.text());
  }

  window.location.reload();
}
