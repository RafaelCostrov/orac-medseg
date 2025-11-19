"""
Módulo auxiliar.auxiliar

Contém decoradores de autenticação/autorização usados nas rotas Flask do projeto.

Funções:
- role_required(*roles): decorator factory que exige que o usuário em sessão tenha um dos papéis informados.
- login_required: decorator que redireciona para a página de login caso não haja usuário em sessão.

Uso:
@role_required("administrador", "gestor")
@login_required
def rota_protegida(...):
    ...
"""
from flask import jsonify, session, redirect, url_for
from functools import wraps


def role_required(*roles):
    """
    Decorator factory que cria um decorator para verificar o papel do usuário.

    Args:
        *roles (str): lista de papéis permitidos para acessar a rota.

    Comportamento:
        - Se não houver usuário em sessão ou o papel não estiver na lista, retorna 403 JSON.
        - Caso contrário, executa a função decorada.
    """
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            usuario = session.get("usuario")
            if not usuario or usuario.get("role") not in roles:
                return jsonify({"erro": "Acesso negado!"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper


def login_required(f):
    """
    Decorator que garante que exista um usuário em sessão.

    Comportamento:
        - Se não houver usuário em sessão, redireciona para a rota de login.
        - Caso contrário, executa a função decorada.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
