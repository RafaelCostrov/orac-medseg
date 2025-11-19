"""
Módulo repository.usuario_repository

Fornece UsuarioRepository para operações de persistência e consulta
da entidade Usuario usando SQLAlchemy.

Classes:
- UsuarioRepository: métodos para salvar, listar, filtrar, buscar por id/email e remover usuários.
"""
from sqlalchemy import func, and_
from model.usuario import Usuario
from db.db import Session


class UsuarioRepository:
    """
    Repositório responsável pelo acesso a dados da entidade Usuario.

    Atributos:
    - session: sessão do SQLAlchemy a ser usada para operações.

    Métodos principais:
    - salvar(usuario): persiste ou atualiza um usuário.
    - listar_todos_usuarios(): retorna todos os usuários.
    - filtrar_usuarios(...): filtra usuários com paginação/ordenação.
    - filtrar_por_id(id_usuario): busca usuário por id.
    - filtrar_por_email(email_usuario): busca usuário por email.
    - remover_usuario(usuario_a_remover): remove usuário passado.
    """

    def __init__(self):
        self.session = Session

    def salvar(self, usuario: Usuario):
        """
        Persiste um usuário (insert ou update).

        Args:
            usuario (Usuario): instância a ser salva.

        Levanta:
            Exception em caso de erro; faz rollback antes de propagar.
        """
        try:
            self.session.add(usuario)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def listar_todos_usuarios(self):
        """
        Retorna todos os usuários da base.

        Returns:
            list[Usuario]: lista de instâncias Usuario.
        """
        try:
            usuarios = self.session.query(Usuario).all()
            return usuarios
        except Exception as e:
            raise e

    def filtrar_usuarios(self, id_usuario=None, nome_usuario=None, email_usuario=None, role=None, offset=None, limit=None,
                         order_by=None, order_dir=None):
        """
        Filtra usuários por vários critérios, com paginação e ordenação.

        Args:
            id_usuario (int|None): filtro por id.
            nome_usuario (str|None): filtro por nome (like, case-insensitive).
            email_usuario (str|None): filtro por email (like).
            role (str|None): filtro por papel.
            offset (int|None), limit (int|None): paginação.
            order_by (str|None), order_dir (str|None): ordenação.

        Returns:
            tuple: (resultados, total, total_filtrado)
        """
        try:
            query = self.session.query(Usuario)
            total = query.count()
            filtros = []
            if id_usuario is not None:
                filtros.append(Usuario.id_usuario == id_usuario)
            if nome_usuario:
                filtros.append(func.lower(
                    Usuario.nome_usuario).like(f"%{nome_usuario}%"))
            if email_usuario:
                filtros.append(func.lower(
                    Usuario.email_usuario).like(f"%{email_usuario}%"))
            if role:
                filtros.append(func.lower(
                    Usuario.role).like(f"%{role}%"))

            query = query.filter(and_(*filtros))

            campos_permitidos = {
                "id_usuario": Usuario.id_usuario,
                "nome_usuario": Usuario.nome_usuario,
                "email_usuario": Usuario.email_usuario,
                "role": Usuario.role
            }

            if order_by in campos_permitidos:
                coluna = campos_permitidos[order_by]
                if order_dir == "desc":
                    coluna = coluna.desc()
                else:
                    coluna = coluna.asc()

                query = query.order_by(coluna)

            total_filtrado = query.count()
            if offset is not None:
                query = query.offset(offset)
            if limit is not None:
                query = query.limit(limit)

            resultados = query.all()
            return resultados, total, total_filtrado
        except Exception as e:
            raise e

    def filtrar_por_id(self, id_usuario):
        """
        Busca um usuário pelo id.

        Args:
            id_usuario (int)

        Returns:
            Usuario|None: instância encontrada ou None.
        """
        try:
            usuario = self.session.query(Usuario).filter(
                Usuario.id_usuario == id_usuario).first()
            return usuario
        except Exception as e:
            raise e

    def filtrar_por_email(self, email_usuario):
        """
        Busca um usuário pelo email.

        Args:
            email_usuario (str)

        Returns:
            Usuario|None: instância encontrada ou None.
        """
        try:
            usuario = self.session.query(Usuario).filter(
                Usuario.email_usuario == email_usuario).first()
            return usuario
        except Exception as e:
            raise e

    def remover_usuario(self, usuario_a_remover):
        """
        Remove o usuário fornecido da sessão e confirma a transação.

        Args:
            usuario_a_remover (Usuario)

        Levanta:
            Exception em caso de erro.
        """
        try:
            self.session.delete(usuario_a_remover)
            self.session.commit()
        except Exception as e:
            raise e
