const requiredFields = document.querySelectorAll('form [required]');
const fields = document.querySelectorAll('form :is(input, textarea)');

requiredFields.forEach(field => {
  const fieldLabel = field.previousElementSibling;
  if (!fieldLabel) return;
  fieldLabel.textContent += ' *';
})

const onlyNumbers = value => value.replace(/\D/g, '');

const formatCPF = value => {
  let newValue = onlyNumbers(value).slice(0, 11);
  return newValue.replace(/(\d{3})(\d{0,3})(\d{0,3})(\d{0,2})/, (match, p1, p2, p3, p4) => (
    p1 + (p2 ? `.${p2}` : '') + (p3 ? `.${p3}` : '') + (p4 ? `-${p4}` : '')
  ));
}

const formatCNPJ = value => {
  let newValue = onlyNumbers(value).slice(0, 14);
  return newValue.replace(/(\d{2})(\d{0,3})(\d{0,3})(\d{0,4})(\d{0,2})/, (match, p1, p2, p3, p4, p5) => (
    p1 + (p2 ? `.${p2}` : '') + (p3 ? `.${p3}` : '') + (p4 ? `/${p4}` : '') + (p5 ? `-${p5}` : '')
  ));
}

const formatPhone = value => {
  let newValue = onlyNumbers(value);
  if (newValue.length <= 11) {
    return newValue.replace(/(\d{2})(\d{0,5})(\d{0,4})/, (match, p1, p2, p3) => (
      `(${p1}) ${p2}` + (p3 ? `-${p3}` : '')
    ));
  }
  newValue = newValue.slice(0, 13);
  return newValue.replace(/(\d{2})(\d{0,2})(\d{0,5})(\d{0,4})/, (match, p1, p2, p3, p4) => (
    `+${p1} (${p2}) ${p3}` + (p4 ? `-${p4}` : '')
  ));
}

const formatCEP = value => {
  let newValue = onlyNumbers(value).slice(0, 8);
  return newValue.replace(/(\d{5})(\d{0,3})/, '$1-$2');
}

const formatRG = value => {
  let newValue = onlyNumbers(value).slice(0, 14);
  return newValue;
}

const formatMoney = value => {
  let newValue = `${parseInt(onlyNumbers(value) ?? 0)}`;
  if (newValue === 'NaN'|| !newValue) newValue = '0';
  if (newValue.length <= 2) {
    return `R$ 0,${newValue.padStart(2, '0')}`;
  }
  const decimal = newValue.slice(-2);
  newValue = newValue.slice(0, -2);
  return `R$ ${newValue},${decimal}`;
}

const validatePastDate = value => {
  const newValue = onlyNumbers(value);
  if (newValue.length !== 8) return false;
  
  const [year, month, day] = [parseInt(newValue.slice(0, 4)), parseInt(newValue.slice(4, 6)), parseInt(newValue.slice(6, 8))];
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth() + 1;
  const currentDay = currentDate.getDate();

  return !(year > currentYear || 
    (year === currentYear && month > currentMonth) || 
    (year === currentYear && month === currentMonth && day > currentDay));
}

const validateFutureDate = v => !validatePastDate(v);

const formatField = (field, formatter = null, validator = null) => {
  if (formatter) {
    field.value = formatter(field.value);
  }
  field.addEventListener('input', event => {
    if (event.inputType === 'deleteContentBackward') return;
    const { value } = event.target;
    const formattedValue = formatter ? formatter(value) : value;
    event.target.value = formattedValue;
    if (validator && !validator(value)) {
      event.target.value = "";
    };
  });
}

const formatPercent = value => {
  let newValue = parseFloat(onlyNumbers(value)) ?? 0;
  return newValue + '%';
}

setFields = () => {
  const fields = document.querySelectorAll('form :is(input, textarea)');
  fields.forEach(field => {
    const dataType = field.getAttribute('data-type')?.toLowerCase() ?? '';
    
    if (!dataType && field.type === 'text') {
      field.addEventListener('input', event => {
        if (event.inputType !== 'deleteContentBackward') {
          event.target.value = event.target.value.toUpperCase();
        }
      });
      return;
    }

    switch (dataType) {
      case 'cpf':
        field.type = "text";
        formatField(field, formatCPF);
        break;
      case 'cep':
        field.type = "text";
        formatField(field, formatCEP);
        break;
      case 'phone':
        formatField(field, formatPhone);
        break;
      case 'pastdate':
        formatField(field, null, validatePastDate);
        break;
      case 'futuredate':
        formatField(field, null, validateFutureDate);
        break;
      case 'cnpj':
        field.type = "text";
        formatField(field, formatCNPJ);
        break;
      case 'percent':
        field.type = "text";
        formatField(field, formatPercent);
        break;
      case 'rg':
        field.type = "text";
        formatField(field, formatRG);
        break;
      case 'money':
        field.type = "text";
        formatField(field, formatMoney);
        break;
    }
  });
}

setFields();

async function listaCidade(estadoID) {
  if (!estadoID || estadoID === "new") return;

  const cidadeSelect = document.querySelector("#cidade_id");
  const response = await fetch(`/local/estados/${estadoID}/cidades/`);
  if (!response.ok) return;
  const data = await response.json();
  data.forEach(cidadeItem => {
    const option = document.createElement("option");
    option.value = cidadeItem.id;
    option.textContent = cidadeItem.nome_cidade;
    cidadeSelect.appendChild(option);
  })
}
