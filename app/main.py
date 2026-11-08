from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import schemas
from app.database import Base, engine, get_db
from app.models import Movimentacao, Produto
from app.pricing import custo_medio_ponderado

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API de Estoque",
    version="1.0.0",
    lifespan=lifespan
)

def obter_produto(
    db: Session,
    produto_id: int,
    *,
    travar: bool = False
) -> Produto:
    stmt = select(Produto).where(Produto.id == produto_id)

    if travar:
        stmt = stmt.with_for_update()

    produto = db.scalars(stmt).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    return produto


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/produtos",
    response_model=schemas.ProdutoOut,
    status_code=status.HTTP_201_CREATED
)
def criar_produto(
    dados: schemas.ProdutoCreate,
    db: Session = Depends(get_db)
):
    produto = Produto(**dados.model_dump())

    db.add(produto)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="SKU já cadastrado"
        )

    db.refresh(produto)

    return produto


@app.get(
    "/produtos",
    response_model=list[schemas.ProdutoOut]
)
def listar_produtos(
    estoque_max: int | None = None,
    db: Session = Depends(get_db)
):
    stmt = select(Produto).order_by(Produto.id)

    if estoque_max is not None:
        stmt = stmt.where(Produto.estoque <= estoque_max)

    return db.scalars(stmt).all()

@app.get(
    "/produtos/{produto_id}",
    response_model=schemas.ProdutoOut
)
def detalhar_produto(
    produto_id: int,
    db: Session = Depends(get_db)
):
    return obter_produto(db, produto_id)

@app.patch(
    "/produtos/{produto_id}/margem",
    response_model=schemas.ProdutoOut
)
def atualizar_margem(
    produto_id: int,
    dados: schemas.MargemUpdate,
    db: Session = Depends(get_db)
):
    produto = obter_produto(db, produto_id)

    produto.margem_percentual = dados.margem_percentual

    db.commit()
    db.refresh(produto)

    return produto

@app.post(
    "/produtos/{produto_id}/compras",
    response_model=schemas.ProdutoOut,
    status_code=status.HTTP_201_CREATED
)
def registrar_compra(
    produto_id: int,
    dados: schemas.CompraIn,
    db: Session = Depends(get_db)
):
    produto = obter_produto(db, produto_id, travar=True)

    produto.custo_medio_centavos = custo_medio_ponderado(
        produto.estoque,
        produto.custo_medio_centavos,
        dados.quantidade,
        dados.custo_unitario_centavos
    )

    produto.estoque += dados.quantidade

    movimentacao = Movimentacao(
        produto_id=produto.id,
        tipo="entrada",
        quantidade=dados.quantidade,
        custo_unitario_centavos=dados.custo_unitario_centavos
    )

    db.add(movimentacao)

    db.commit()
    db.refresh(produto)

    return produto

@app.post(
    "/produtos/{produto_id}/saidas",
    response_model=schemas.ProdutoOut,
    status_code=status.HTTP_201_CREATED
)
def registrar_saida(
    produto_id: int,
    dados: schemas.SaidaIn,
    db: Session = Depends(get_db)
):
    produto = obter_produto(db, produto_id, travar=True)

    if dados.quantidade > produto.estoque:
        disponivel = produto.estoque
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Estoque insuficiente: disponível {disponivel}, "
                f"pedido {dados.quantidade}"
            )
        )

    produto.estoque -= dados.quantidade

    movimentacao = Movimentacao(
        produto_id=produto.id,
        tipo="saida",
        quantidade=dados.quantidade
    )

    db.add(movimentacao)

    db.commit()
    db.refresh(produto)

    return produto
