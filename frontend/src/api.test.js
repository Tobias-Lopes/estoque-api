
import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest'

import { api, mensagemDeErro } from './api'

describe('mensagemDeErro', () => {
  it('utiliza detail em texto', () => {
    const corpo = {
      detail: 'SKU já cadastrado',
    }

    expect(mensagemDeErro(corpo, 409)).toBe(
      'SKU já cadastrado'
    )
  })

  it('combina mensagens de validação', () => {
    const corpo = {
      detail: [
        { msg: 'Campo obrigatório' },
        { msg: 'Valor inválido' },
      ],
    }

    expect(mensagemDeErro(corpo, 422)).toBe(
      'Campo obrigatório; Valor inválido'
    )
  })

  it('retorna mensagem padrão', () => {
    expect(mensagemDeErro({}, 500)).toBe(
      'Erro 500 ao comunicar com a API'
    )
  })
})


afterEach(() => {
  vi.unstubAllGlobals()
})

describe('requisições HTTP', () => {
  it('lista produtos pela API', async () => {
    const produtos = [
      {
        id: 1,
        sku: 'CAF-001',
        nome: 'Café',
      },
    ]

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => produtos,
    })

    vi.stubGlobal('fetch', fetchMock)

    const resultado = await api.listarProdutos()

    expect(resultado).toEqual(produtos)

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/produtos',
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
  })
  
    it('envia um produto via POST', async () => {
    const dados = {
        sku: 'TEC-001',
        nome: 'Teclado',
        margem_percentual: 30,
    }

    const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ id: 1, ...dados }),
    })

    vi.stubGlobal('fetch', fetchMock)

    const resultado = await api.criarProduto(dados)

    expect(resultado.id).toBe(1)

    expect(fetchMock).toHaveBeenCalledWith(
        '/api/produtos',
        {
        headers: {
            'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify(dados),
        }
    )
    })
    
    it('trata erro de SKU duplicado', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
        ok: false,
        status: 409,
        json: async () => ({
        detail: 'SKU já cadastrado',
        }),
    })

    vi.stubGlobal('fetch', fetchMock)

    const dados = {
        sku: 'CAF-001',
        nome: 'Café',
        margem_percentual: 30,
    }

    await expect(
        api.criarProduto(dados)
    ).rejects.toThrow('SKU já cadastrado')
    })

})
