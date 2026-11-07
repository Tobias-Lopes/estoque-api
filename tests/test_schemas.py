
import pytest

from pydantic import ValidationError

from app.schemas import ProdutoCreate, CompraIn, SaidaIn


def test_produto_com_margem_padrao():
    produto = ProdutoCreate(
        sku="CAF-001",
        nome="Café 500g"
    )

    assert produto.margem_percentual == 30


def test_produto_com_margem_negativa():
    with pytest.raises(ValidationError):
        ProdutoCreate(
            sku="CAF-001",
            nome="Café",
            margem_percentual=-10
        )


def test_compra_com_quantidade_invalida():
    with pytest.raises(ValidationError):
        CompraIn(
            quantidade=0,
            custo_unitario_centavos=1000
        )


def test_saida_com_quantidade_valida():
    saida = SaidaIn(quantidade=5)

    assert saida.quantidade == 5
