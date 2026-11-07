def calcular_preco(custo_medio_centavos: int, margem_percentual: int) -> int:
    return(custo_medio_centavos * (100 + margem_percentual) + 50) // 100