
import pandas as pd

from scripts.importar_csv import validar


def criar_dataframe(linhas):
    return pd.DataFrame(
        linhas,
        columns=["sku", "nome", "margem_percentual"]
    )


def test_csv_valido():
    dados = criar_dataframe([
        ["A", "Café", "30"],
        ["B", "Açúcar", "25"]
    ])

    assert validar(dados) == []


def test_margem_invalida():
    dados = criar_dataframe([
        ["A", "Café", "30"],
        ["B", "Açúcar", "abc"]
    ])

    erros = validar(dados)

    assert len(erros) == 1
    assert "Linha 3" in erros[0]
    assert "margem" in erros[0]


def test_sku_duplicado_e_vazio():
    dados = criar_dataframe([
        ["A", "Café", "30"],
        [" A ", "Café 2", "30"],
        ["", "Produto", "10"]
    ])

    erros = validar(dados)

    assert any("repetido" in erro for erro in erros)
    assert any("sku vazio" in erro for erro in erros)


def test_coluna_ausente():
    dados = pd.DataFrame({
        "sku": ["A"]
    })

    erros = validar(dados)

    assert "Colunas ausentes" in erros[0]
