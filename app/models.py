from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    
    movimentacoes: Mapped[list["Movimentacao"]] = relationship(
        back_populates="produto",
        order_by="Movimentacao.id"
    )


    @property
    def preco_venda_centavos(self) -> int:
        return calcular_preco(
            self.custo_medio_centavos,
            self.margem_percentual
        )


def agora() -> datetime:
    return datetime.now(timezone.utc)


class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id: Mapped[int] = mapped_column(primary_key=True)

    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.id"),
        index=True
    )

    tipo: Mapped[str] = mapped_column(String(10))

    quantidade: Mapped[int]

    custo_unitario_centavos: Mapped[int | None] = mapped_column(
        default=None
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=agora
    )

    produto: Mapped[Produto] = relationship(
        back_populates="movimentacoes"
    )
