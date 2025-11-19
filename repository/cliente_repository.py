"""
Módulo repository.cliente_repository

Fornece a classe ClienteRepository para operações CRUD e de filtragem
sobre a entidade Cliente usando SQLAlchemy.

Classes:
- ClienteRepository: métodos para adicionar, listar, filtrar, atualizar e remover clientes.
"""
from sqlalchemy import func, and_, distinct
from sqlalchemy.orm import joinedload
from model.exame import Exame
from model.cliente import Cliente
from db.db import Session


class ClienteRepository:
    """
    Repositório responsável pelo acesso a dados da entidade Cliente.

    Atributos:
    - session: sessão do SQLAlchemy a ser usada para operações.

    Métodos principais:
    - adicionar_cliente(cliente): persiste um novo cliente.
    - listar_todos_clientes(): retorna todos os clientes com exames carregados.
    - filtrar_clientes(...): filtra clientes por vários campos, ordenação e paginação.
    - filtrar_por_id(id_cliente): retorna um cliente por id.
    - filtrar_por_cnpj(cnpj_cliente): retorna um cliente por CNPJ.
    - remover_cliente(id_cliente): remove cliente por id.
    - atualizar_cliente(...): atualiza campos do cliente e relacionamentos.
    """

    def __init__(self):
        self.session = Session

    def adicionar_cliente(self, cliente: Cliente):
        """
        Adiciona um novo cliente ao banco.

        Args:
            cliente (Cliente): instância de Cliente a ser persistida.

        Levanta:
            Exception em caso de erro; faz rollback antes de propagar.
        """
        try:
            self.session.add(cliente)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def listar_todos_clientes(self):
        """
        Lista todos os clientes, incluindo exames relacionados.

        Returns:
            list[Cliente]: lista de instâncias Cliente.
        """
        try:
            clientes = self.session.query(Cliente).options(
                joinedload(Cliente.exames_incluidos)).all()
            return clientes
        except Exception as e:
            raise e

    def filtrar_clientes(self, id_cliente=None, nome_cliente=None, cnpj_cliente=None, tipo_cliente=None, exames_incluidos=None, offset=None,
                         limit=None, order_by=None, order_dir=None):
        """
        Filtra clientes por diversos critérios, com suporte a paginação e ordenação.

        Args:
            id_cliente (int|None): filtro por id.
            nome_cliente (str|None): filtro por nome (like, case-insensitive).
            cnpj_cliente (str|None): filtro por CNPJ (like, case-insensitive).
            tipo_cliente (list|None): lista de TiposCliente para filtrar.
            exames_incluidos (list[int]|None): lista de ids de exames; retorna clientes que possuem esses exames.
            offset (int|None): deslocamento para paginação.
            limit (int|None): limite de resultados.
            order_by (str|None): campo para ordenação.
            order_dir (str|None): 'asc' ou 'desc'.

        Returns:
            tuple: (resultados, total, total_filtrado)
                - resultados: lista de clientes filtrados.
                - total: total de clientes na tabela antes do filtro.
                - total_filtrado: total de clientes após aplicação dos filtros.
        """
        try:
            query = self.session.query(Cliente)
            total = query.count()
            filtros = []

            if id_cliente is not None:
                filtros.append(Cliente.id_cliente == id_cliente)

            if nome_cliente:
                filtros.append(func.lower(
                    Cliente.nome_cliente).like(f"%{nome_cliente}%"))

            if cnpj_cliente:
                filtros.append(func.lower(
                    Cliente.cnpj_cliente).like(f"%{cnpj_cliente}%"))

            if tipo_cliente:
                filtros.append(func.lower(
                    Cliente.tipo_cliente.in_(tipo_cliente)
                ))

            if exames_incluidos:
                query = query.join(Cliente.exames_incluidos)\
                    .filter(Exame.id_exame.in_(exames_incluidos))

            query = query.filter(
                and_(*filtros)).options(joinedload(Cliente.exames_incluidos))

            campos_permitidos = {
                "id_cliente": Cliente.id_cliente,
                "nome_cliente": Cliente.nome_cliente,
                "cnpj_cliente": Cliente.cnpj_cliente,
                "tipo_cliente": Cliente.tipo_cliente
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

    def filtrar_por_id(self, id_cliente):
        """
        Retorna o cliente correspondente ao id fornecido, carregando exames.

        Args:
            id_cliente (int): id do cliente.

        Returns:
            Cliente|None: instância Cliente ou None se não encontrado.
        """
        try:
            cliente = self.session.query(Cliente)\
                .options(joinedload(Cliente.exames_incluidos))\
                .filter(Cliente.id_cliente == id_cliente).first()
            return cliente
        except Exception as e:
            raise e

    def filtrar_por_cnpj(self, cnpj_cliente):
        """
        Retorna o cliente correspondente ao CNPJ fornecido.

        Args:
            cnpj_cliente (str): CNPJ do cliente.

        Returns:
            Cliente|None: instância Cliente ou None se não encontrado.
        """
        try:
            cliente = self.session.query(Cliente)\
                .options(joinedload(Cliente.exames_incluidos))\
                .filter(Cliente.cnpj_cliente == cnpj_cliente).first()
            return cliente
        except Exception as e:
            raise e

    def remover_cliente(self, id_cliente):
        """
        Remove o cliente com o id informado.

        Args:
            id_cliente (int): id do cliente a remover.

        Levanta:
            Exception em caso de erro.
        """
        try:
            cliente_a_remover = self.filtrar_por_id(id_cliente=id_cliente)
            self.session.delete(cliente_a_remover)
            self.session.commit()
        except Exception as e:
            raise e

    def atualizar_cliente(self, id_cliente, nome_cliente, cnpj_cliente, tipo_cliente, exames_incluidos):
        """
        Atualiza campos de um cliente existente.

        Args:
            id_cliente (int): id do cliente a atualizar.
            nome_cliente (str|None): novo nome (se fornecido).
            cnpj_cliente (str|None): novo CNPJ (se fornecido).
            tipo_cliente (TiposCliente|None): novo tipo (se fornecido).
            exames_incluidos (list[Exame]|None): lista de exames relacionados (substitui a lista atual).

        Returns:
            dict: representação simplificada do cliente atualizado.
        """
        try:
            cliente_a_atualizar = self.filtrar_por_id(id_cliente=id_cliente)

            if nome_cliente is not None and nome_cliente != "":
                cliente_a_atualizar.nome_cliente = nome_cliente

            if cnpj_cliente is not None and cnpj_cliente != "":
                cliente_a_atualizar.cnpj_cliente = cnpj_cliente

            if tipo_cliente is not None and tipo_cliente != "":
                cliente_a_atualizar.tipo_cliente = tipo_cliente

            if exames_incluidos is not None:
                cliente_a_atualizar.exames_incluidos = exames_incluidos

            self.session.commit()
            return {
                "id_cliente": cliente_a_atualizar.id_cliente,
                "nome_cliente": cliente_a_atualizar.nome_cliente,
                "cnpj_cliente": cliente_a_atualizar.cnpj_cliente,
                "tipo_cliente": cliente_a_atualizar.tipo_cliente.__str__(),
                "exames_incluidos": cliente_a_atualizar.exames_incluidos,
            }
        except Exception as e:
            self.session.rollback()
            raise e
