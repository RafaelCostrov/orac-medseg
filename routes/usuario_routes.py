"""
Módulo routes.usuario_routes

Define rotas Flask relacionadas à autenticação e gestão de usuários:
- login, logout, reset de senha,
- cadastro, listagem, filtragem, remoção e atualização de usuários,
- exportação para XLS e TXT.

Cada rota usa os decoradores de autenticação/autorização do módulo auxiliar.auxiliar.
"""
from flask import Blueprint, request, jsonify, session, send_file
from services.usuario_service import UsuarioService
from datetime import datetime
from auxiliar.auxiliar import role_required, login_required

usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuarios")

service = UsuarioService()


@usuario_bp.route('/login', methods=['POST'])
def login():
    """
    Rota POST para autenticação de usuário.

    Corpo JSON esperado:
    {
      "email_usuario": str,
      "senha": str
    }

    Retorna:
        200 + dados do usuário em sessão em caso de sucesso,
        401 em credenciais inválidas,
        400 em erro.
    """
    try:
        data = request.get_json()
        email_usuario = data.get('email_usuario')
        senha = data.get('senha')
        usuario = service.verificar_usuario(
            email_usuario=email_usuario, senha=senha)
        if usuario:
            session['usuario'] = {
                "id_usuario": usuario.id_usuario,
                "nome_usuario": usuario.nome_usuario,
                "email_usuario": usuario.email_usuario,
                "role": usuario.role.__str__(),
                "foto_url": usuario.foto_url if usuario.foto_url else None
            }
            return jsonify({
                "mensagem": "Usuário autenticado com sucesso!",
                "usuario": session['usuario']
            }), 200
        else:
            return jsonify({
                "erro": "Email ou senha inválidos!"
            }), 401
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/resetar-senha', methods=['POST'])
def resetar_senha():
    """
    Rota POST para reset de senha.

    Corpo JSON esperado:
    { "email_usuario": str }

    Retorna:
        200 com mensagem de envio em caso de sucesso,
        400 em erro.
    """
    try:
        data = request.get_json()
        email_usuario = data.get('email_usuario')
        email_enviado = service.resetar_senha(
            email_usuario=email_usuario
        )
        return jsonify({
            "mensagem": f"Nova senha enviada no email '{email_enviado}'"
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Rota POST para encerrar a sessão do usuário autenticado.

    Retorna:
        200 em sucesso, 400 em erro.
    """
    try:
        session.pop('usuario', None)
        return jsonify({
            "mensagem": "Usuário deslogado com sucesso!"
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/cadastrar-usuario', methods=['POST'])
@login_required
def cadastrar_usuario():
    """
    Rota POST para cadastro de usuário.

    Espera formulário multipart com campos:
    nome_usuario, email_usuario, senha, role e opcionalmente foto.

    Retorna:
        201 com dados do usuário criado, 400 em erro ou conflito de email.
    """
    try:
        data = request.form
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        senha = data.get('senha')
        role = data.get('role')
        foto = request.files.get('foto')

        novo_usuario = service.cadastrar_usuario(
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
            senha=senha,
            foto=foto if foto else None
        )

        if "Email já cadastrado" in novo_usuario.get("erro", ""):
            return jsonify(novo_usuario), 400

        return jsonify({
            "mensagem": f"Usuário cadastrado!",
            **novo_usuario
        }), 201
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro! Tente novamente"
        }), 400


@usuario_bp.route('/listar-usuarios')
@login_required
def listar_todos_usuarios():
    """
    Rota GET que retorna todos os usuários.

    Retorna:
        200 com lista de usuários em JSON, 400 em erro.
    """
    try:
        usuarios = service.listar_todos_usuarios()
        return jsonify({
            "mensagem": "Usuários listadas com sucesso!",
            "usuarios": usuarios
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/filtrar-usuarios', methods=['POST'])
@login_required
def filtrar_usuario():
    """
    Rota POST para filtragem de usuários.

    Corpo JSON aceita filtros e paginação:
    id_usuario, nome_usuario, email_usuario, role, pagina, por_pagina, order_by, order_dir
    """
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        role = data.get('role')
        pagina = data.get('pagina', 1)
        por_pagina = data.get('por_pagina', 20)
        order_by = data.get('order_by')
        order_dir = data.get('order_dir')

        usuarios_filtrados = service.filtrar_usuarios(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
            pagina=pagina,
            por_pagina=por_pagina,
            order_by=order_by,
            order_dir=order_dir
        )
        return jsonify({
            "mensagem": "Usuários filtradas com sucesso!",
            **usuarios_filtrados
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/remover-usuario', methods=['DELETE'])
@login_required
@role_required("administrador")
def remover_usuario():
    """
    Rota DELETE para remoção de usuário por id.

    Corpo JSON esperado:
    { "id_usuario": int }

    Restrições:
    - um usuário não pode remover sua própria conta (retorna 403).
    - requer papel administrador.
    """
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        if int(id_usuario) == int(session['usuario']['id_usuario']):
            return jsonify({
                "erro": "Você não pode excluir sua própria conta!"
            }), 403

        service.remover_usuario(id_usuario=id_usuario)
        return ({
            "mensagem": "Usuario removido com sucesso!"
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/atualizar-usuario', methods=['PUT'])
@login_required
@role_required("administrador")
def atualizar_usuario():
    """
    Rota PUT para atualização de usuário (administrador).

    Espera formulário multipart com campos atualizáveis:
    id_usuario, nome_usuario, email_usuario, senha, role, foto

    Retorna:
        200 com dados atualizados ou 400 em erro.
    """
    try:
        data = request.form
        id_usuario = data.get('id_usuario')
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        senha = data.get('senha')
        role = data.get('role')
        foto = request.files.get('foto')
        role = data.get('role')

        usuario_atualizado = service.atualizar_usuario(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            senha=senha,
            role=role,
            foto=foto if foto else None
        )
        # session["usuario"] = usuario_atualizado

        return ({
            "mensagem": "Usuário atualizado com sucesso!",
            **usuario_atualizado
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/atualizar-conta', methods=['PUT'])
@login_required
def atualizar_conta():
    """
    Rota PUT para atualização da própria conta do usuário autenticado.

    Valida que o id fornecido corresponde ao usuário em sessão.
    """
    try:
        data = request.form
        id_usuario = data.get('id_usuario')
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        senha = data.get('senha')
        role = data.get('role')
        foto = request.files.get('foto')

        if id_usuario != str(session['usuario']['id_usuario']):
            return jsonify({
                "erro": "Você só pode atualizar sua própria conta!"
            }), 403

        usuario_atualizado = service.atualizar_usuario(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            senha=senha,
            role=role,
            foto=foto if foto else None
        )
        session["usuario"] = usuario_atualizado

        return ({
            "mensagem": "Conta atualizada com sucesso!",
            **usuario_atualizado
        }), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/exportar-usuarios-xls', methods=['POST'])
@login_required
def exportar_excel():
    """
    Rota POST que gera e envia um arquivo .xlsx com usuários filtrados.
    """
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        role = data.get('role')

        arquivo = service.exportar_excel(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
        )

        agora = datetime.now()
        hora = agora.strftime("%H-%M-%S")
        nome_excel = f"Usuarios_{hora}.xlsx"

        return send_file(
            arquivo,
            download_name=nome_excel,
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400


@usuario_bp.route('/exportar-usuarios-txt', methods=['POST'])
@login_required
def exportar_txt():
    """
    Rota POST que gera e envia um arquivo .txt (tab separated) com usuários filtrados.
    """
    try:
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        nome_usuario = data.get('nome_usuario')
        email_usuario = data.get('email_usuario')
        role = data.get('role')

        arquivo = service.exportar_txt(
            id_usuario=id_usuario,
            nome_usuario=nome_usuario,
            email_usuario=email_usuario,
            role=role,
        )

        agora = datetime.now()
        hora = agora.strftime("%H-%M-%S")
        nome_txt = f"Usuarios_{hora}.txt"

        return send_file(
            arquivo,
            download_name=nome_txt,
            as_attachment=True,
            mimetype="text/plain"
        )

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "erro": "Ocorreu um erro, tente novamente!"
        }), 400
