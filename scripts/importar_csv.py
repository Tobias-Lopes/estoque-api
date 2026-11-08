
import sys

import httpx
import pandas as pd


COLUNAS = {"sku", "nome", "margem_percentual"}


def validar(df: pd.DataFrame) -> list[str]:
    faltando = COLUNAS - set(df.columns)

    if faltando:
        return [f"Colunas ausentes: {sorted(faltando)}"]

    erros = []

    skus = df["sku"].str.strip()
    repetidos = set(skus[skus.duplicated(keep=False)])

    for indice, linha in df.iterrows():
        numero_linha = indice + 2

        sku = linha["sku"].strip()
        nome = linha["nome"].strip()

        if not sku:
            erros.append(f"Linha {numero_linha}: sku vazio")
        elif len(sku) > 40:
            erros.append(f"Linha {numero_linha}: sku muito longo")
        elif sku in repetidos:
            erros.append(
                f"Linha {numero_linha}: sku '{sku}' repetido no arquivo"
            )

        if not nome:
            erros.append(f"Linha {numero_linha}: nome vazio")
        elif len(nome) > 120:
            erros.append(f"Linha {numero_linha}: nome muito longo")

        try:
            margem = int(linha["margem_percentual"])

            if not 0 <= margem <= 500:
                erros.append(
                    f"Linha {numero_linha}: margem fora de 0-500"
                )

        except ValueError:
            erros.append(
                f"Linha {numero_linha}: margem não é número inteiro"
            )

    return erros

def main(caminho: str, base_url: str) -> int:
    df = pd.read_csv(
        caminho,
        dtype=str,
        keep_default_na=False
    )

    erros = validar(df)

    if erros:
        print(
            "Importação cancelada. Corrija:\n- "
            + "\n- ".join(erros)
        )
        return 1

    with httpx.Client(base_url=base_url) as client:
        for produto in df.to_dict("records"):
            response = client.post(
                "/produtos",
                json={
                    "sku": produto["sku"].strip(),
                    "nome": produto["nome"].strip(),
                    "margem_percentual": int(
                        produto["margem_percentual"]
                    )
                }
            )

            response.raise_for_status()

    print(f"{len(df)} produtos importados.")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(
            "Uso: python -m scripts.importar_csv "
            "<arquivo.csv> <url_da_api>"
        )

    sys.exit(main(sys.argv[1], sys.argv[2]))
