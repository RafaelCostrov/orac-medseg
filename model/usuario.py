"""
Módulo model.usuario

Define o modelo SQLAlchemy Usuario e operações simples relacionadas à senha.
"""
from sqlalchemy import Column, Integer, String, Enum
from enums.tipos_usuario import TiposUsuario
from werkzeug.security import generate_password_hash, check_password_hash
from db.db import Base


class Usuario(Base):
    """
    Modelo SQLAlchemy para a tabela 'usuario'.

    Atributos:
    - id_usuario (int): chave primária autoincrement.
    - nome_usuario (str): nome do usuário.
    - email_usuario (str): email único e obrigatório.
    - senha (str): hash da senha.
    - role (Enum): papel do usuário (TiposUsuario).
    - foto_url (str|None): URL da foto armazenada externamente.

    Métodos:
    - setar_senha(senha): armazena hash da senha.
    - checkar_senha(senha): verifica senha em relação ao hash.
    """
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column(String(100))
    email_usuario = Column(String(100), unique=True, nullable=False)
    senha = Column(String(200))
    role = Column(Enum(TiposUsuario))
    foto_url = Column(String(200), nullable=True)

    def setar_senha(self, senha):
        """
        Gera e define o hash da senha para o usuário.

        Args:
            senha (str)
        """
        self.senha = generate_password_hash(senha)

    def checkar_senha(self, senha):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            senha (str)

        Returns:
            bool
        """
        return check_password_hash(self.senha, senha)
