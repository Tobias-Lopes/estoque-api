
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.pricing import calcular_preco


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)

    sku: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        index=True
    )

    nome: Mapped[str] = mapped_column(String(120))

    estoque: Mapped[int] = mapped_column(default=0)

    custo_medio_centavos: Mapped[int] = mapped_column(
        default=0
    )

    margem_percentual: Mapped[int] = mapped_column(
        default=30
    )

    @property
    def preco_venda_centavos(self) -> int:
        return calcular_preco(
            self.custo_medio_centavos,
            self.margem_percentual
        )
