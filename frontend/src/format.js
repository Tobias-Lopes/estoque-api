
const brl = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

export function formatarCentavos(centavos) {
  return brl.format(centavos / 100)
}

export function reaisParaCentavos(texto) {
  const numero = Number(
    String(texto).trim().replace(',', '.')
  )

  if (!Number.isFinite(numero)) {
    return NaN
  }

  return Math.round(numero * 100)
}
