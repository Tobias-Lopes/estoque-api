
def criar_produto(
    client,
    sku="CAF-001",
    margem=50
):
    return client.post(
        "/produtos",
        json={
            "sku": sku,
            "nome": "Café 500g",
            "margem_percentual": margem
        }
    )


def test_criar_produto(client):
    response = criar_produto(client)

    assert response.status_code == 201

    produto = response.json()

    assert produto["sku"] == "CAF-001"
    assert produto["estoque"] == 0
    assert produto["margem_percentual"] == 50


def test_sku_duplicado(client):
    criar_produto(client)

    response = criar_produto(client)

    assert response.status_code == 409


def test_compra_atualiza_custo_medio(client):
    produto = criar_produto(client).json()
    produto_id = produto["id"]

    client.post(
        f"/produtos/{produto_id}/compras",
        json={
            "quantidade": 10,
            "custo_unitario_centavos": 1000
        }
    )

    response = client.post(
        f"/produtos/{produto_id}/compras",
        json={
            "quantidade": 10,
            "custo_unitario_centavos": 2000
        }
    )

    assert response.status_code == 201

    dados = response.json()

    assert dados["estoque"] == 20
    assert dados["custo_medio_centavos"] == 1500
    assert dados["preco_venda_centavos"] == 2250


def test_saida_atualiza_estoque(client):
    produto_id = criar_produto(client).json()["id"]

    client.post(
        f"/produtos/{produto_id}/compras",
        json={
            "quantidade": 10,
            "custo_unitario_centavos": 1000
        }
    )

    response = client.post(
        f"/produtos/{produto_id}/saidas",
        json={"quantidade": 4}
    )

    assert response.status_code == 201
    assert response.json()["estoque"] == 6
    assert response.json()["custo_medio_centavos"] == 1000


def test_estoque_insuficiente(client):
    produto_id = criar_produto(client).json()["id"]

    response = client.post(
        f"/produtos/{produto_id}/saidas",
        json={"quantidade": 5}
    )

    assert response.status_code == 409

    produto = client.get(
        f"/produtos/{produto_id}"
    ).json()

    assert produto["estoque"] == 0


def test_quantidade_invalida(client):
    produto_id = criar_produto(client).json()["id"]

    response = client.post(
        f"/produtos/{produto_id}/saidas",
        json={"quantidade": 0}
    )

    assert response.status_code == 422


def test_produto_inexistente(client):
    response = client.get("/produtos/999999")

    assert response.status_code == 404


def test_atualizar_margem(client):
    produto_id = criar_produto(client).json()["id"]

    client.post(
        f"/produtos/{produto_id}/compras",
        json={
            "quantidade": 1,
            "custo_unitario_centavos": 1000
        }
    )

    response = client.patch(
        f"/produtos/{produto_id}/margem",
        json={"margem_percentual": 100}
    )

    assert response.status_code == 200
    assert response.json()["preco_venda_centavos"] == 2000


def test_filtro_estoque_baixo(client):
    primeiro = criar_produto(client, sku="A").json()["id"]
    segundo = criar_produto(client, sku="B").json()["id"]

    client.post(
        f"/produtos/{primeiro}/compras",
        json={
            "quantidade": 2,
            "custo_unitario_centavos": 100
        }
    )

    client.post(
        f"/produtos/{segundo}/compras",
        json={
            "quantidade": 50,
            "custo_unitario_centavos": 100
        }
    )

    response = client.get(
        "/produtos",
        params={"estoque_max": 5}
    )

    skus = [produto["sku"] for produto in response.json()]

    assert skus == ["A"]


def test_historico_movimentacoes(client):
    produto_id = criar_produto(client).json()["id"]

    client.post(
        f"/produtos/{produto_id}/compras",
        json={
            "quantidade": 5,
            "custo_unitario_centavos": 100
        }
    )

    client.post(
        f"/produtos/{produto_id}/saidas",
        json={"quantidade": 2}
    )

    response = client.get(
        f"/produtos/{produto_id}/movimentacoes"
    )

    assert response.status_code == 200

    historico = response.json()

    assert len(historico) == 2
    assert historico[0]["tipo"] == "entrada"
    assert historico[0]["quantidade"] == 5
    assert historico[0]["custo_unitario_centavos"] == 100

    assert historico[1]["tipo"] == "saida"
    assert historico[1]["quantidade"] == 2
    assert historico[1]["custo_unitario_centavos"] is None