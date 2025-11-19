"""
Módulo db.db

Configura a conexão e o escopo de sessão SQLAlchemy para a aplicação Flask.

Variáveis/objetos exportados:
- Base: declarative_base() usado para modelos.
- engine: engine SQLAlchemy conectado ao banco (lê SENHA_BD do .env).
- SessionFactory: factory de sessões.
- Session: scoped_session para uso em todo o projeto (thread-safe).
- Base.metadata.create_all(engine) é executado para garantir que as tabelas existam.

Observações:
- A URL do banco é construída com a variável de ambiente SENHA_BD.
- Ajuste as variáveis no .env conforme necessário.
"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

SENHA_BD = os.getenv("SENHA_BD")
DATABASE_URL = f"mysql+mysqlconnector://costrov:{SENHA_BD}@localhost/orac_med"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_timeout=30,
)

SessionFactory = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False)
Session = scoped_session(SessionFactory)

Base.metadata.create_all(engine)
