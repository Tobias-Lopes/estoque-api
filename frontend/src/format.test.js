
import { describe, expect, it } from 'vitest'

import {
  formatarCentavos,
  reaisParaCentavos,
} from './format'

describe('reaisParaCentavos', () => {
  it('aceita vírgula e ponto', () => {
    expect(reaisParaCentavos('10,50')).toBe(1050)
    expect(reaisParaCentavos('10.50')).toBe(1050)
  })

  it('não perde centavos por ponto flutuante', () => {
    expect(reaisParaCentavos('19.99')).toBe(1999)
  })

  it('retorna NaN para texto inválido', () => {
    expect(reaisParaCentavos('abc')).toBeNaN()
  })
})

describe('formatarCentavos', () => {
  it('formata valores em reais', () => {
    const resultado = formatarCentavos(1500)

    expect(resultado.replace(/\s/g, ' ')).toBe('R$ 15,00')
  })
})
