from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.database import Base, engine, get_db
from app.models import Produto


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API de Estoque",
    version="1.0.0",
    lifespan=lifespan
)


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
