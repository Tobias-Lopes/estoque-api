def calcular_preco(custo_medio_centavos: int, margem_percentual: int) -> int:
    return(custo_medio_centavos * (100 + margem_percentual) + 50) // 100

def custo_medio_ponderado(
    estoque_atual: int,
    custo_atual_centavos: int,
    qtd_compra: int,
    custo_compra_centavos: int
) -> int:
    novo_estoque = estoque_atual + qtd_compra

    total = (
        estoque_atual * custo_atual_centavos
        + qtd_compra * custo_compra_centavos
    )

    return (2 * total + novo_estoque) // (2 * novo_estoque)
