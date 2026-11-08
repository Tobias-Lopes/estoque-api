
from app.pricing import calcular_preco, custo_medio_ponderado

def test_preco_com_margem():
    resultado = calcular_preco(1000, 50)
    assert resultado == 1500


def test_preco_arredonda_para_cima():
    resultado = calcular_preco(101, 50)
    assert resultado == 152


def test_margem_zero_mantem_custo():
    resultado = calcular_preco(1234, 0)
    assert resultado == 1234

def test_primeira_compra_define_custo_medio():
    resultado = custo_medio_ponderado(
        0, 0, 10, 1000
    )

    assert resultado == 1000


def test_compra_recalcula_custo_medio():
    resultado = custo_medio_ponderado(
        10, 1000, 10, 2000
    )

    assert resultado == 1500


def test_custo_medio_arredonda_meio_centavo():
    resultado = custo_medio_ponderado(
        1, 100, 1, 101
    )

    assert resultado == 101
