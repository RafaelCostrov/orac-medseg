"""
Módulo services.usuario_service

Camada de serviço para operações de negócio relacionadas a Usuario:
- validações básicas (ex.: email duplicado),
- manipulação de foto via Google Drive,
- geração e reset de senha,
- exportação para Excel e TXT.
"""
from model.usuario import Usuario
from repository.usuario_repository import UsuarioRepository
from enums.tipos_usuario import TiposUsuario
from services.google_services.envio_drive import salvar_drive, remover_drive
from services.google_services.envio_email import enviar
import os
import random
import string
import pandas as pd
from io import BytesIO


class UsuarioService():
    """
    Serviço de alto nível para gerenciar usuários.

    Atributos:
    - repositorio: instância de UsuarioRepository.

    Métodos principais:
    - verificar_usuario(email, senha): autenticação básica.
    - cadastrar_usuario(...): cria usuário e envia foto ao Drive.
    - listar_todos_usuarios(): retorna usuários em JSON serializável.
    - filtrar_usuarios(...): filtragem com paginação/ordenação.
    - remover_usuario(id_usuario): remove usuário e exclui foto do Drive.
    - atualizar_usuario(...): atualiza campos e foto.
    - gerar_senha(), resetar_senha(email): utilitários para senhas.
    - exportar_excel(...), exportar_txt(...): geram arquivos para download.
    """
    repositorio = UsuarioRepository()

    def verificar_usuario(self, email_usuario: str, senha: str):
        """
        Valida credenciais e retorna a instância do usuário ou None.

        Args:
            email_usuario (str), senha (str)

        Returns:
            Usuario|None
        """
        usuarios, _, _ = self.repositorio.filtrar_usuarios(
            email_usuario=email_usuario)
        usuario = usuarios[0] if usuarios else None
        if usuario and usuario.checkar_senha(senha):
            return usuario
        return None

    def cadastrar_usuario(self, nome_usuario: str,  email_usuario: str, role: TiposUsuario, senha: str, foto=None):
        """
        Registra um novo usuário, faz upload da foto se fornecida e retorna representação serializável.

        Args:
            nome_usuario (str), email_usuario (str), role (TiposUsuario), senha (str), foto (FileStorage|None)

        Returns:
            dict: dados do usuário criado ou dict com chave "erro" em caso de conflito.
        """
        usuario_email = self.repositorio.filtrar_por_email(
            email_usuario=email_usuario)

        if usuario_email:
            return {
                "erro": "Email já cadastrado."
            }

        usuario = Usuario(
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role
        )

        if foto is not None:
            nome_arquivo = foto.filename
            os.makedirs("services\\temp_uploads", exist_ok=True)
            temp_path = os.path.join("services\\temp_uploads", nome_arquivo)
            foto.save(temp_path)
            foto_url = salvar_drive(
                temp_path, usuario.email_usuario, usuario.nome_usuario)
            usuario.foto_url = foto_url
            os.remove(temp_path)

        usuario.setar_senha(senha)
        self.repositorio.salvar(usuario=usuario)

        return {
            "id_usuario": usuario.id_usuario,
            "nome_usuario": usuario.nome_usuario,
            "email_usuario": usuario.email_usuario,
            "role": usuario.role.__str__(),
            "foto_url": usuario.foto_url if usuario.foto_url else None
        }

    def listar_todos_usuarios(self):
        """
        Retorna lista de todos os usuários em formato JSON serializável.

        Returns:
            list[dict]
        """
        usuarios = self.repositorio.listar_todos_usuarios()
        lista = []
        for usuario in usuarios:
            json_usuario = {
                "id_usuario": usuario.id_usuario,
                "nome_usuario": usuario.nome_usuario,
                "email_usuario": usuario.email_usuario,
                "role": usuario.role.__str__()
            }
            lista.append(json_usuario)
        return lista

    def filtrar_usuarios(self, id_usuario: int, nome_usuario: str,  email_usuario: str, role: TiposUsuario, por_pagina=50, pagina: int = 1,
                         order_by: str = "nome_usuario", order_dir: str = "desc"):
        """
        Filtra usuários delegando ao repositório e formata o resultado.

        Args:
            mesmos filtros de repository.filtrar_usuarios mais paginação e ordenação.

        Returns:
            dict: {'usuarios': [...], 'total': int, 'total_filtrado': int}
        """
        if por_pagina is not None:
            offset = (pagina - 1) * por_pagina
        else:
            offset = None

        usuarios_filtrados, total, total_filtrado = self.repositorio.filtrar_usuarios(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
            offset=offset,
            limit=por_pagina,
            order_by=order_by,
            order_dir=order_dir
        )
        lista_filtrada = []
        for usuario in usuarios_filtrados:
            json_usuario = {
                "id_usuario": usuario.id_usuario,
                "nome_usuario": usuario.nome_usuario,
                "email_usuario": usuario.email_usuario,
                "role": usuario.role.__str__(),
            }
            lista_filtrada.append(json_usuario)
        return {
            "usuarios": lista_filtrada,
            "total": total,
            "total_filtrado": total_filtrado
        }

    def remover_usuario(self, id_usuario):
        """
        Remove um usuário por id, removendo sua foto do Drive quando existir.

        Args:
            id_usuario (int)
        """
        usuario_a_remover = self.repositorio.filtrar_por_id(
            id_usuario=id_usuario)
        if not usuario_a_remover:
            raise Exception("Usuário não encontrado")
        if usuario_a_remover.foto_url is not None:
            remover_drive(usuario_a_remover.foto_url)
        self.repositorio.remover_usuario(usuario_a_remover=usuario_a_remover)

    def atualizar_usuario(self, id_usuario, nome_usuario, email_usuario, senha, role, foto):
        """
        Atualiza campos de um usuário (nome, email, senha, role e foto).

        Faz upload da nova foto para o Drive e remove a anterior se necessário.

        Returns:
            dict: representação serializável do usuário atualizado.
        """
        usuario = self.repositorio.filtrar_por_id(id_usuario=id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado")

        if nome_usuario and nome_usuario.strip():
            usuario.nome_usuario = nome_usuario

        if email_usuario and email_usuario.strip():
            usuario.email_usuario = email_usuario

        if role:
            usuario.role = role

        if senha and senha.strip():
            usuario.setar_senha(senha)

        if foto:
            if usuario.foto_url:
                remover_drive(usuario.foto_url)
            nome_arquivo = foto.filename
            os.makedirs("services\\temp_uploads", exist_ok=True)
            temp_path = os.path.join("services\\temp_uploads", nome_arquivo)
            foto.save(temp_path)
            foto_url = salvar_drive(
                temp_path, usuario.email_usuario, usuario.nome_usuario)
            usuario.foto_url = foto_url
            os.remove(temp_path)

        self.repositorio.salvar(usuario)

        return {
            "id_usuario": usuario.id_usuario,
            "nome_usuario": usuario.nome_usuario,
            "email_usuario": usuario.email_usuario,
            "role": usuario.role.__str__(),
            "foto_url": usuario.foto_url
        }

    def gerar_senha(self):
        """
        Gera uma senha aleatória contendo maiúsculas, minúsculas, números e caracteres especiais.

        Returns:
            str: nova senha gerada.
        """
        letras_maiusculas = random.choice(string.ascii_uppercase)
        letras_minusculas = random.choice(string.ascii_lowercase)
        numeros = random.choice(string.digits)
        especiais = random.choice("!@#$%&?")
        todos = string.ascii_letters + string.digits + "!@#$%&?"
        restante = ''.join(random.choice(todos) for _ in range(8))
        senha = letras_maiusculas + letras_minusculas + numeros + especiais + restante
        senha = ''.join(random.sample(senha, len(senha)))
        return senha

    def resetar_senha(self, email_usuario: str):
        """
        Reseta a senha de um usuário e envia a nova senha por email.

        Args:
            email_usuario (str)

        Returns:
            bool|str: resultado do envio de email (depende da implementação do enviar()).
        """
        usuario = self.repositorio.filtrar_por_email(
            email_usuario=email_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado")
        nova_senha = self.gerar_senha()
        self.atualizar_usuario(id_usuario=usuario.id_usuario, nome_usuario=None,
                               email_usuario=None, role=None, foto=None, senha=nova_senha)
        email_enviado = enviar(email_usuario=email_usuario,
                               nome_usuario=usuario.nome_usuario, nova_senha=nova_senha)

        return email_enviado

    def exportar_excel(self, id_usuario: int, nome_usuario: str,  email_usuario: str, role: TiposUsuario):
        """
        Gera um BytesIO contendo um Excel com os usuários filtrados.

        Returns:
            BytesIO
        """
        usuarios_filtrados = self.filtrar_usuarios(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
            por_pagina=None
        )

        linhas = []
        for usuario in usuarios_filtrados.get("usuarios"):
            linha = {**usuario}
            linhas.append(linha)

        novos_cabecalhos = {
            "id_usuario": "ID Usuario",
            "nome_usuario": "Nome",
            "email_usuario": "Email",
            "role": "Nível de Acesso"
        }

        map_role = {
            "usuario": "Usuário",
            "gestor": "Gestor",
            "administrador": "Administrador",
        }

        df = pd.DataFrame(linhas)
        df["role"] = df["role"].map(
            map_role)
        df.rename(columns=novos_cabecalhos, inplace=True)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name='Atendimentos', index=False)
        output.seek(0)

        return output

    def exportar_txt(self, id_usuario: int, nome_usuario: str,  email_usuario: str, role: TiposUsuario):
        """
        Gera um BytesIO contendo um TXT (tab-separated) com os usuários filtrados.

        Returns:
            BytesIO
        """
        usuarios_filtrados = self.filtrar_usuarios(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
            por_pagina=None
        )

        linhas = []
        for usuario in usuarios_filtrados.get("usuarios"):
            linha = {**usuario}
            linhas.append(linha)

        novos_cabecalhos = {
            "id_usuario": "ID Usuario",
            "nome_usuario": "Nome",
            "email_usuario": "Email",
            "role": "Nível de Acesso"
        }

        map_role = {
            "usuario": "Usuário",
            "gestor": "Gestor",
            "administrador": "Administrador",
        }

        df = pd.DataFrame(linhas)
        df["role"] = df["role"].map(
            map_role)
        df.rename(columns=novos_cabecalhos, inplace=True)
        output = BytesIO()
        df.to_csv(output, sep="\t", index=False, encoding="utf-8")
        output.seek(0)

        return output
