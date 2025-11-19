"""
Módulo model.exame

Define o modelo SQLAlchemy Exame, representando os exames disponíveis no sistema.

Classe:
- Exame: colunas id_exame, nome_exame, is_interno, valor_exame.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from db.db import Base


class Exame(Base):
    """
    Modelo SQLAlchemy para a tabela 'exame'.

    Atributos:
    - id_exame (int): chave primária autoincrement.
    - nome_exame (str): nome do exame.
    - is_interno (bool): indica se o exame é interno.
    - valor_exame (float): valor cobrado pelo exame.
    """
    __tablename__ = 'exame'

    id_exame = Column(Integer, primary_key=True, autoincrement=True)
    nome_exame = Column(String(100))
    is_interno = Column(Boolean)
    valor_exame = Column(Float)
