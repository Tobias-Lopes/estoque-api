
const BASE_URL = '/api'

export function mensagemDeErro(corpo, status) {
  const detail = corpo?.detail

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail.map((erro) => erro.msg).join('; ')
  }

  return `Erro ${status} ao comunicar com a API`
}

async function request(caminho, opcoes = {}) {
  let response

  try {
    response = await fetch(BASE_URL + caminho, {
      headers: { 'Content-Type': 'application/json' },
      ...opcoes,
    })
  } catch {
    throw new Error('Não foi possível conectar à API')
  }

  if (!response.ok) {
    const corpo = await response.json().catch(() => ({}))
    throw new Error(mensagemDeErro(corpo, response.status))
  }

  return response.json()
}

function post(caminho, dados) {
  return request(caminho, {
    method: 'POST',
    body: JSON.stringify(dados),
  })
}

export const api = {
  listarProdutos: (estoqueMax = null) =>
    request(
      estoqueMax === null
        ? '/produtos'
        : `/produtos?estoque_max=${estoqueMax}`
    ),

  criarProduto: (dados) =>
    post('/produtos', dados),

  registrarCompra: (id, dados) =>
    post(`/produtos/${id}/compras`, dados),

  registrarSaida: (id, dados) =>
    post(`/produtos/${id}/saidas`, dados),
}
