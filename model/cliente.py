"""
Módulo model.cliente

Define a entidade Cliente e a tabela associativa cliente_exame.
"""
from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from enums.tipos_cliente import TiposCliente
from db.db import Base


cliente_exame = Table(
    'cliente_exame',
    Base.metadata,
    Column('id_cliente', Integer, ForeignKey(
        'cliente.id_cliente'), primary_key=True),
    Column('id_exame', Integer, ForeignKey('exame.id_exame'), primary_key=True)
)


class Cliente(Base):
    """
    Modelo SQLAlchemy para a tabela 'cliente'.

    Atributos de coluna:
    - id_cliente (int): chave primária autoincrement.
    - nome_cliente (str): nome do cliente.
    - cnpj_cliente (str): CNPJ sem formatação.
    - tipo_cliente (Enum): valor do enum TiposCliente.
    - exames_incluidos (list[Exame]): relação many-to-many com Exame via cliente_exame.
    """
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String(100))
    cnpj_cliente = Column(String(14))
    tipo_cliente = Column(Enum(TiposCliente))
    exames_incluidos = relationship(
        "Exame", secondary=cliente_exame, backref="cliente")
