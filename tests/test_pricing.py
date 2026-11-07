
from app.pricing import calcular_preco


def test_preco_com_margem():
    resultado = calcular_preco(1000, 50)
    assert resultado == 1500


def test_preco_arredonda_para_cima():
    resultado = calcular_preco(101, 50)
    assert resultado == 152


def test_margem_zero_mantem_custo():
    resultado = calcular_preco(1234, 0)
    assert resultado == 1234
