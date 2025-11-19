
"""
Módulo model.atendimento

Define o modelo SQLAlchemy Atendimento e a tabela associativa atendimento_exame.

Classe:
- Atendimento: representa um atendimento realizado, relacionando-se a Cliente e Exame.
"""
from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from enums.tipos_atendimento import TiposAtendimento
from db.db import Base


atendimento_exame = Table(
    'atendimento_exame',
    Base.metadata,
    Column('id_atendimento', Integer, ForeignKey(
        'atendimento.id_atendimento'), primary_key=True),
    Column('id_exame', Integer, ForeignKey('exame.id_exame'), primary_key=True)
)


class Atendimento(Base):
    """
    Modelo SQLAlchemy para a tabela 'atendimento'.

    Atributos de coluna:
    - id_atendimento (int): chave primária autoincrement.
    - data_atendimento (datetime): data e hora do atendimento.
    - tipo_atendimento (Enum): valor do enum TiposAtendimento.
    - usuario (str): nome do atendente.
    - valor (float): valor cobrado pelo atendimento.
    - colaborador_atendimento (str): colaborador vinculado.
    - is_ativo (bool): status do atendimento.
    - id_cliente (int): FK para cliente.
    - cliente_atendimento (Cliente): relação many-to-one com Cliente.
    - exames_atendimento (list[Exame]): relação many-to-many com Exame via atendimento_exame.
    """
    __tablename__ = 'atendimento'

    id_atendimento = Column(Integer, primary_key=True, autoincrement=True)
    data_atendimento = Column(DateTime)
    tipo_atendimento = Column(Enum(TiposAtendimento))
    usuario = Column(String(100))
    valor = Column(Float)
    colaborador_atendimento = Column(String(100))
    is_ativo = Column(Boolean)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))
    cliente_atendimento = relationship(
        "Cliente", backref="atendimento")
    exames_atendimento = relationship(
        "Exame", secondary=atendimento_exame, backref="atendimento")
