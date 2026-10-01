const elements = {
  error: document.querySelector("#error-message"),
  form: document.querySelector("#transaction-form"),
  type: document.querySelector("#transaction-type"),
  value: document.querySelector("#transaction-value"),
  description: document.querySelector("#transaction-description"),
  submitButton: document.querySelector("#submit-button"),
  loading: document.querySelector("#loading-state"),
  empty: document.querySelector("#empty-state"),
  list: document.querySelector("#transaction-list"),
};

let transactions = [];
let hasLoaded = false;

const apiMessages = {
  "description cannot be empty": "Informe uma descrição.",
  "value must be a valid decimal": "Informe um valor válido.",
  "value must be greater than zero": "O valor deve ser maior que zero.",
  "transaction_type must be 'income' or 'expense'": "Selecione um tipo válido.",
  "internal server error": "O servidor encontrou um erro. Tente novamente.",
};

function showError(message) {
  elements.error.hidden = false;
  elements.error.textContent = message;
}

function clearError() {
  elements.error.textContent = "";
  elements.error.hidden = true;
}

function setLoading(isLoading) {
  elements.loading.hidden = !isLoading;
  if (isLoading) {
    elements.empty.hidden = true;
    elements.list.hidden = true;
  }
}

async function readResponse(response) {
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error(`A API retornou uma resposta inválida (HTTP ${response.status}).`);
  }

  if (!response.ok) {
    const detail = data && typeof data.error === "string" ? data.error : "";
    throw new Error(apiMessages[detail] || detail || `A operação falhou (HTTP ${response.status}).`);
  }

  return data;
}

const currencyFormatter = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
  minimumFractionDigits: 2,
  maximumFractionDigits: 20,
});

function formatValue(value) {
  const text = String(value);
  return /^\d+(?:\.\d+)?$/.test(text)
    ? currencyFormatter.format(text)
    : `R$ ${text}`;
}

function renderTransactions(items) {
  const rows = items.map((transaction) => {
    const row = document.createElement("li");
    row.className = "transaction-item";

    const details = document.createElement("div");
    details.className = "transaction-details";

    const description = document.createElement("strong");
    description.className = "transaction-description";
    description.textContent = transaction.description;

    const meta = document.createElement("div");
    meta.className = "transaction-meta";

    const id = document.createElement("span");
    id.textContent = `ID ${transaction.id}`;

    const type = document.createElement("span");
    type.className = `type-label ${transaction.type === "income" ? "income" : "expense"}`;
    type.textContent = transaction.type === "income" ? "Entrada" : "Despesa";

    const amount = document.createElement("span");
    amount.className = `transaction-amount ${transaction.type === "income" ? "income" : "expense"}`;
    amount.textContent = formatValue(transaction.value);

    meta.append(id, type);
    details.append(description, meta);
    row.append(details, amount);
    return row;
  });

  elements.list.replaceChildren(...rows);
  elements.empty.hidden = items.length !== 0;
  elements.list.hidden = items.length === 0;
}

async function loadTransactions() {
  clearError();
  setLoading(true);

  try {
    const response = await fetch("/transactions");
    const data = await readResponse(response);
    if (!Array.isArray(data)) {
      throw new Error("A API retornou uma lista de transações inválida.");
    }
    transactions = data;
    hasLoaded = true;
  } catch (error) {
    showError(error instanceof TypeError
      ? "Não foi possível conectar à API. Verifique se o servidor está ativo."
      : error.message);
  } finally {
    setLoading(false);
    if (hasLoaded) {
      renderTransactions(transactions);
    }
  }
}

async function createTransaction(event) {
  event.preventDefault();
  clearError();

  const payload = {
    transaction_type: elements.type.value,
    value: elements.value.value.trim().replace(",", "."),
    description: elements.description.value.trim(),
  };

  elements.submitButton.disabled = true;
  elements.submitButton.textContent = "Adicionando…";
  try {
    const response = await fetch("/transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const created = await readResponse(response);
    if (response.status !== 201) {
      throw new Error(`A API retornou uma resposta inesperada (HTTP ${response.status}).`);
    }

    elements.form.reset();
    transactions = [...transactions, created];
    hasLoaded = true;
    renderTransactions(transactions);
    await loadTransactions();
  } catch (error) {
    showError(error instanceof TypeError
      ? "Não foi possível conectar à API. Verifique se o servidor está ativo."
      : error.message);
  } finally {
    elements.submitButton.disabled = false;
    elements.submitButton.textContent = "Adicionar transação";
  }
}

elements.form.addEventListener("submit", createTransaction);
loadTransactions();
