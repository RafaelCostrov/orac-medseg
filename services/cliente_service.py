"""
Módulo services.cliente_service

Contém a camada de serviço para operações de negócio relacionadas a Cliente:
- validações simples (ex.: CNPJ duplicado),
- transformação de modelos para JSON,
- exportação para Excel e TXT,
- integração com serviço externo para consulta de nome por CNPJ.
"""
from model.cliente import Cliente
from repository.cliente_repository import ClienteRepository
from repository.exame_repository import ExameRepository
from enums.tipos_cliente import TiposCliente
import pandas as pd
from io import BytesIO
import requests


class ClienteService():
    """
    Serviço de alto nível para gerenciar clientes.

    Atributos:
    - repositorio: instância de ClienteRepository.
    - repositorio_exame: instância de ExameRepository.

    Métodos expostos:
    - cadastrar_cliente(...)
    - listar_todos_clientes()
    - filtrar_clientes(...)
    - remover_cliente(id_cliente)
    - atualizar_cliente(...)
    - buscar_cnpj(cnpj)
    - exportar_excel(...)
    - exportar_txt(...)
    """
    repositorio = ClienteRepository()
    repositorio_exame = ExameRepository()

    def cadastrar_cliente(self, nome_cliente: str, cnpj_cliente: str, tipo_cliente: TiposCliente, exames_incluidos: list[int]):
        """
        Registra um novo cliente após validação de CNPJ duplicado.

        Args:
            nome_cliente (str)
            cnpj_cliente (str)
            tipo_cliente (TiposCliente)
            exames_incluidos (list[int]): lista de ids de exames.

        Returns:
            dict|None: dicionário com erro quando houver CNPJ duplicado, caso contrário None.
        """
        cliente_cnpj = self.repositorio.filtrar_por_cnpj(
            cnpj_cliente=cnpj_cliente)

        if cliente_cnpj:
            return {
                "erro": "CNPJ já cadastrado."
            }

        exames = []
        if exames_incluidos is not None:
            for exame_id in exames_incluidos:
                exame = self.repositorio_exame.filtrar_por_id(exame_id)
                exames.append(exame)
        cliente = Cliente(
            nome_cliente=nome_cliente,
            cnpj_cliente=cnpj_cliente,
            tipo_cliente=tipo_cliente,
            exames_incluidos=exames
        )
        self.repositorio.adicionar_cliente(cliente=cliente)

    def listar_todos_clientes(self):
        """
        Retorna todos os clientes formatados em JSON serializável.

        Returns:
            list[dict]: lista de clientes com seus exames no formato dicionário.
        """
        clientes = self.repositorio.listar_todos_clientes()
        lista = []
        for cliente in clientes:
            exames = []
            for exame in cliente.exames_incluidos:
                json_exame = {
                    "id_exame": exame.id_exame,
                    "nome_exame": exame.nome_exame,
                    "valor_exame": exame.valor_exame,
                    "is_interno": exame.is_interno
                }
                exames.append(json_exame)
            json_cliente = {
                "id_cliente": cliente.id_cliente,
                "nome_cliente": cliente.nome_cliente,
                "cnpj_cliente": cliente.cnpj_cliente,
                "tipo_cliente": cliente.tipo_cliente.__str__(),
                "exames_incluidos": exames
            }
            lista.append(json_cliente)
        return lista

    def filtrar_clientes(self, id_cliente: int, nome_cliente: str, cnpj_cliente: str, tipo_cliente: list[TiposCliente],
                         exames_incluidos: list[int], por_pagina=50, pagina: int = 1,
                         order_by: str = "nome_cliente", order_dir: str = "desc"):
        """
        Realiza a filtragem de clientes delegando ao repositório e formatando o resultado.

        Args:
            id_cliente, nome_cliente, cnpj_cliente, tipo_cliente, exames_incluidos: filtros.
            por_pagina (int|None): quantos itens por página (None para sem paginação).
            pagina (int): página atual.
            order_by (str), order_dir (str): ordenação.

        Returns:
            dict: {'clientes': [...], 'total': int, 'total_filtrado': int}
        """
        if por_pagina is not None:
            offset = (pagina - 1) * por_pagina
        else:
            offset = None

        clientes_filtrados, total, total_filtrado = self.repositorio.filtrar_clientes(
            id_cliente=id_cliente,
            nome_cliente=nome_cliente,
            cnpj_cliente=cnpj_cliente,
            tipo_cliente=tipo_cliente,
            exames_incluidos=exames_incluidos,
            offset=offset,
            limit=por_pagina,
            order_by=order_by,
            order_dir=order_dir
        )

        lista_filtrada = []
        for cliente in clientes_filtrados:
            exames = []
            for exame in cliente.exames_incluidos:
                json_exame = {
                    "id_exame": exame.id_exame,
                    "nome_exame": exame.nome_exame,
                    "valor_exame": exame.valor_exame,
                    "is_interno": exame.is_interno
                }
                exames.append(json_exame)
            json_cliente = {
                "id_cliente": cliente.id_cliente,
                "nome_cliente": cliente.nome_cliente,
                "cnpj_cliente": cliente.cnpj_cliente,
                "tipo_cliente": cliente.tipo_cliente.__str__(),
                "exames_incluidos": exames
            }
            lista_filtrada.append(json_cliente)
        return {
            "clientes": lista_filtrada,
            "total": total,
            "total_filtrado": total_filtrado
        }

    def remover_cliente(self, id_cliente):
        """
        Remove cliente por id.

        Args:
            id_cliente (int)
        """
        self.repositorio.remover_cliente(id_cliente=id_cliente)

    def atualizar_cliente(self, id_cliente: int, nome_cliente: str, cnpj_cliente: str, tipo_cliente: TiposCliente, exames_incluidos: list[int]):
        """
        Atualiza um cliente existente e retorna sua representação JSON.

        Verifica duplicidade de CNPJ antes de persistir.

        Returns:
            dict: cliente atualizado em formato serializável ou dict {'erro': ...}.
        """
        cliente = self.repositorio.filtrar_por_id(id_cliente=id_cliente)

        cliente_cnpj = self.repositorio.filtrar_por_cnpj(
            cnpj_cliente=cnpj_cliente)
        if cliente_cnpj and cnpj_cliente != cliente.cnpj_cliente:
            return {
                "erro": "CNPJ já cadastrado."
            }

        if exames_incluidos is not None:
            exames = []
            for exame_id in exames_incluidos:
                exame = self.repositorio_exame.filtrar_por_id(exame_id)
                exames.append(exame)
        else:
            exames = cliente.exames_incluidos
        cliente_atualizado = self.repositorio.atualizar_cliente(
            id_cliente=id_cliente,
            nome_cliente=nome_cliente,
            cnpj_cliente=cnpj_cliente,
            tipo_cliente=tipo_cliente,
            exames_incluidos=exames
        )
        exames_json = []
        for exames_atualizado in cliente_atualizado.get('exames_incluidos'):
            json_exame = {
                "id_exame": exames_atualizado.id_exame,
                "nome_exame": exames_atualizado.nome_exame,
                "valor_exame": exames_atualizado.valor_exame,
                "is_interno": exames_atualizado.is_interno
            }
            exames_json.append(json_exame)

        json_cliente = {
            "id_cliente": cliente_atualizado.get('id_cliente'),
            "nome_cliente": cliente_atualizado.get('nome_cliente'),
            "cnpj_cliente": cliente_atualizado.get('cnpj_cliente'),
            "tipo_cliente": cliente_atualizado.get('tipo_cliente'),
            "exames_incluidos": exames_json
        }
        return json_cliente

    def buscar_cnpj(self, cnpj: str):
        """
        Consulta um serviço externo (receitaws) para recuperar o nome da empresa pelo CNPJ.

        Args:
            cnpj (str)

        Returns:
            str|None: nome retornado pela API ou None se indisponível.
        """
        url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
        headers = {
            "User-Agent": "orac-med/1.0",
            "X-System-Name": "orac-med"
        }
        requisicao = requests.get(url, headers=headers)
        resposta = requisicao.json()
        nome = resposta.get("nome")
        return nome

    def exportar_excel(self, id_cliente: int, nome_cliente: str, cnpj_cliente: str, tipo_cliente: TiposCliente, exames_incluidos: list[int]):
        """
        Gera um arquivo Excel (BytesIO) com os clientes filtrados.

        Args:
            mesmos filtros de filtrar_clientes

        Returns:
            BytesIO: arquivo Excel pronto para envio via Flask send_file.
        """
        clientes_filtrados = self.filtrar_clientes(
            id_cliente=id_cliente,
            nome_cliente=nome_cliente,
            cnpj_cliente=cnpj_cliente,
            tipo_cliente=tipo_cliente,
            exames_incluidos=exames_incluidos,
            por_pagina=None
        )

        linhas = []
        for cliente in clientes_filtrados.get("clientes"):
            nomes_exames = [exame.get("nome_exame") for exame in cliente.get(
                "exames_incluidos", [])]
            exames_str = ", ".join(nomes_exames)
            cliente["exames_incluidos"] = exames_str
            linha = {**cliente}
            linhas.append(linha)

        novos_cabecalhos = {
            "id_cliente": "ID Cliente",
            "nome_cliente": "Nome",
            "cnpj_cliente": "CNPJ",
            "tipo_cliente": "Tipo",
            "usuario": "Atendente",
            "exames_incluidos": "Exames inclusos"
        }

        map_tipos_cliente = {
            "cliente": "Cliente",
            "credenciado": "Credenciado",
            "servico_prestado": "Serviço Prestado",
            "particular": "Particular",
        }

        df = pd.DataFrame(linhas)
        df["tipo_cliente"] = df["tipo_cliente"].map(
            map_tipos_cliente)
        df.rename(columns=novos_cabecalhos, inplace=True)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name='Atendimentos', index=False)
        output.seek(0)

        return output

    def exportar_txt(self, id_cliente: int, nome_cliente: str, cnpj_cliente: str, tipo_cliente: TiposCliente, exames_incluidos: list[int]):
        """
        Gera um arquivo TXT (tab-separated) com os clientes filtrados.

        Returns:
            BytesIO: fluxo pronto para envio.
        """
        clientes_filtrados = self.filtrar_clientes(
            id_cliente=id_cliente,
            nome_cliente=nome_cliente,
            cnpj_cliente=cnpj_cliente,
            tipo_cliente=tipo_cliente,
            exames_incluidos=exames_incluidos,
            por_pagina=None
        )

        linhas = []
        for cliente in clientes_filtrados.get("clientes"):
            nomes_exames = [exame.get("nome_exame") for exame in cliente.get(
                "exames_incluidos", [])]
            exames_str = ", ".join(nomes_exames)
            cliente["exames_incluidos"] = exames_str
            linha = {**cliente}
            linhas.append(linha)

        novos_cabecalhos = {
            "id_cliente": "ID Cliente",
            "nome_cliente": "Nome",
            "cnpj_cliente": "CNPJ",
            "tipo_cliente": "Tipo",
            "usuario": "Atendente",
            "exames_incluidos": "Exames inclusos"
        }

        map_tipos_cliente = {
            "cliente": "Cliente",
            "credenciado": "Credenciado",
            "servico_prestado": "Serviço Prestado",
            "particular": "Particular",
        }

        df = pd.DataFrame(linhas)
        df["tipo_cliente"] = df["tipo_cliente"].map(
            map_tipos_cliente)
        df.rename(columns=novos_cabecalhos, inplace=True)
        output = BytesIO()
        df.to_csv(output, sep="\t", index=False, encoding="utf-8")
        output.seek(0)

        return output
