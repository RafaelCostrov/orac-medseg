# Pydoc gerado em 2025-11-18 21:22:43


---

## Módulo: main

Python Library Documentation: module main

NAME
    main - Módulo main

DESCRIPTION
    Inicializa a aplicação Flask, registra blueprints e define rotas de páginas
    (frontend) que exigem autenticação quando aplicável.

    Comportamento:
    - Cria o app Flask e configura CORS e secret_key.
    - Registra os blueprints: exame, cliente, usuario e atendimento.
    - Define rotas que retornam templates: login, redefinir, atendimento, relatorio, conta, cadastro.
    - As rotas que exibem páginas protegidas utilizam o decorator login_required do módulo auxiliar.auxiliar.

    Execução:
        python main.py
    ou
        set FLASK_APP=main.py && flask run
    (ajuste host/port conforme necessário).

FUNCTIONS
    atendimento()

    cadastro()

    conta()

    login()

    redefinir()

    relatorio()

DATA
    app = <Flask 'main'>
    atendimento_bp = <Blueprint 'atendimento'>
    cliente_bp = <Blueprint 'cliente'>
    exame_bp = <Blueprint 'exame'>
    session = <LocalProxy unbound>
    usuario_bp = <Blueprint 'usuario'>

FILE
    c:\users\rafae\desktop\orac-medseg\main.py



---

## Módulo: db.db

Python Library Documentation: module db.db in db

NAME
    db.db - Módulo db.db

DESCRIPTION
    Configura a conexão e o escopo de sessão SQLAlchemy para a aplicação Flask.

    Variáveis/objetos exportados:
    - Base: declarative_base() usado para modelos.
    - engine: engine SQLAlchemy conectado ao banco (lê SENHA_BD do .env).
    - SessionFactory: factory de sessões.
    - Session: scoped_session para uso em todo o projeto (thread-safe).
    - Base.metadata.create_all(engine) é executado para garantir que as tabelas existam.

    Observações:
    - A URL do banco é construída com a variável de ambiente SENHA_BD.
    - Ajuste as variáveis no .env conforme necessário.

DATA
    DATABASE_URL = 'mysql+mysqlconnector://costrov:Senha181!@localhost/ora...
    SENHA_BD = 'Senha181!'
    Session = <sqlalchemy.orm.scoping.scoped_session object>
    SessionFactory = sessionmaker(class_='Session', bind=Engine(mysql...ac...
    engine = Engine(mysql+mysqlconnector://costrov:***@localhost/orac_med)

FILE
    c:\users\rafae\desktop\orac-medseg\db\db.py



---

## Módulo: auxiliar.auxiliar

Python Library Documentation: module auxiliar.auxiliar in auxiliar

NAME
    auxiliar.auxiliar - Módulo auxiliar.auxiliar

DESCRIPTION
    Contém decoradores de autenticação/autorização usados nas rotas Flask do projeto.

    Funções:
    - role_required(*roles): decorator factory que exige que o usuário em sessão tenha um dos papéis informados.
    - login_required: decorator que redireciona para a página de login caso não haja usuário em sessão.

    Uso:
    @role_required("administrador", "gestor")
    @login_required
    def rota_protegida(...):
        ...

FUNCTIONS
    login_required(f)
        Decorator que garante que exista um usuário em sessão.

        Comportamento:
            - Se não houver usuário em sessão, redireciona para a rota de login.
            - Caso contrário, executa a função decorada.

    role_required(*roles)
        Decorator factory que cria um decorator para verificar o papel do usuário.

        Args:
            *roles (str): lista de papéis permitidos para acessar a rota.

        Comportamento:
            - Se não houver usuário em sessão ou o papel não estiver na lista, retorna 403 JSON.
            - Caso contrário, executa a função decorada.

DATA
    session = <LocalProxy unbound>

FILE
    c:\users\rafae\desktop\orac-medseg\auxiliar\auxiliar.py



---

## Módulo: model.exame

Python Library Documentation: module model.exame in model

NAME
    model.exame - Módulo model.exame

DESCRIPTION
    Define o modelo SQLAlchemy Exame, representando os exames disponíveis no sistema.

    Classe:
    - Exame: colunas id_exame, nome_exame, is_interno, valor_exame.

CLASSES
    sqlalchemy.orm.decl_api.Base(builtins.object)
        Exame

    class Exame(sqlalchemy.orm.decl_api.Base)
     |  Exame(**kwargs)
     |
     |  Modelo SQLAlchemy para a tabela 'exame'.
     |
     |  Atributos:
     |  - id_exame (int): chave primária autoincrement.
     |  - nome_exame (str): nome do exame.
     |  - is_interno (bool): indica se o exame é interno.
     |  - valor_exame (float): valor cobrado pelo exame.
     |
     |  Method resolution order:
     |      Exame
     |      sqlalchemy.orm.decl_api.Base
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs) from sqlalchemy.orm.instrumentation
     |      A simple constructor that allows initialization from kwargs.
     |
     |      Sets attributes on the constructed instance using the names and
     |      values in ``kwargs``.
     |
     |      Only keys that are present as
     |      attributes of the instance's class are allowed. These could be,
     |      for example, any mapped columns or relationships.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  id_exame
     |
     |  is_interno
     |
     |  nome_exame
     |
     |  valor_exame
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  __mapper__ = <Mapper at 0x2b169f94ad0; Exame>
     |
     |  __table__ = Table('exame', MetaData(), Column('id_exame', In...lor_exa...
     |
     |  __tablename__ = 'exame'
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __abstract__ = True
     |
     |  metadata = MetaData()
     |
     |  registry = <sqlalchemy.orm.decl_api.registry object>

FILE
    c:\users\rafae\desktop\orac-medseg\model\exame.py



---

## Módulo: repository.exame_repository

Python Library Documentation: module repository.exame_repository in repository

NAME
    repository.exame_repository - Módulo repository.exame_repository

DESCRIPTION
    Fornece ExameRepository para operações CRUD e de filtragem sobre a
    entidade Exame usando SQLAlchemy.

    Classe:
    - ExameRepository: métodos para adicionar, listar, filtrar, atualizar e remover exames.

CLASSES
    builtins.object
        ExameRepository

    class ExameRepository(builtins.object)
     |  Repositório responsável pelo acesso a dados da entidade Exame.
     |
     |  Atributos:
     |  - session: sessão do SQLAlchemy a ser usada para operações.
     |
     |  Métodos principais:
     |  - adicionar_exame(exame): persiste um novo exame.
     |  - listar_todos_exames(): retorna todos os exames.
     |  - filtrar_exames(...): filtra exames por vários campos, ordenação e paginação.
     |  - filtrar_por_id(id_exame): retorna um exame por id.
     |  - remover_exame(id_exame): remove exame por id.
     |  - atualizar_exame(...): atualiza campos do exame.
     |
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  adicionar_exame(self, exame: model.exame.Exame)
     |      Adiciona um novo exame ao banco.
     |
     |      Args:
     |          exame (Exame): instância de Exame a ser persistida.
     |
     |      Levanta:
     |          Exception em caso de erro; faz rollback antes de propagar.
     |
     |  atualizar_exame(self, id_exame, nome_exame, is_interno, valor_exame)
     |      Atualiza campos de um exame existente.
     |
     |      Args:
     |          id_exame (int): id do exame a atualizar.
     |          nome_exame (str|None): novo nome (se fornecido).
     |          is_interno (bool|None): marca como interno/externo (se fornecido).
     |          valor_exame (float|None): novo valor (se fornecido).
     |
     |      Returns:
     |          dict: representação simplificada do exame atualizado.
     |
     |  filtrar_exames(
     |      self,
     |      id_exame=None,
     |      nome_exame=None,
     |      is_interno=None,
     |      min_valor=None,
     |      max_valor=None,
     |      offset=None,
     |      limit=None,
     |      order_by=None,
     |      order_dir=None
     |  )
     |      Filtra exames por diversos critérios, com suporte a paginação e ordenação.
     |
     |      Args:
     |          id_exame (int|None): filtro por id.
     |          nome_exame (str|None): filtro por nome (like, case-insensitive).
     |          is_interno (bool|None): filtro por interno/externo.
     |          min_valor (float|None): valor mínimo.
     |          max_valor (float|None): valor máximo.
     |          offset (int|None): deslocamento para paginação.
     |          limit (int|None): limite de resultados.
     |          order_by (str|None): campo para ordenação.
     |          order_dir (str|None): 'asc' ou 'desc'.
     |
     |      Returns:
     |          tuple: (resultados, total, total_filtrado)
     |              - resultados: lista de exames filtrados.
     |              - total: total de exames na tabela antes do filtro.
     |              - total_filtrado: total após aplicação dos filtros.
     |
     |  filtrar_por_id(self, id_exame)
     |      Retorna o exame correspondente ao id fornecido.
     |
     |      Args:
     |          id_exame (int): id do exame.
     |
     |      Returns:
     |          Exame|None: instância Exame ou None se não encontrado.
     |
     |  listar_todos_exames(self)
     |      Lista todos os exames.
     |
     |      Returns:
     |          list[Exame]: lista de instâncias Exame.
     |
     |  remover_exame(self, id_exame)
     |      Remove o exame com o id informado.
     |
     |      Args:
     |          id_exame (int): id do exame a remover.
     |
     |      Levanta:
     |          Exception em caso de erro.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

DATA
    Session = <sqlalchemy.orm.scoping.scoped_session object>
    func = <sqlalchemy.sql.functions._FunctionGenerator object>

FILE
    c:\users\rafae\desktop\orac-medseg\repository\exame_repository.py



---

## Módulo: services.exame_service

Python Library Documentation: module services.exame_service in services

NAME
    services.exame_service - Módulo services.exame_service

DESCRIPTION
    Camada de serviço para operações de negócio relacionadas a Exame:
    - validação mínima,
    - transformação de modelos para JSON,
    - exportação para Excel e TXT.

CLASSES
    builtins.object
        ExameService

    class ExameService(builtins.object)
     |  Serviço de alto nível para gerenciar exames.
     |
     |  Atributos:
     |  - repositorio: instância de ExameRepository.
     |
     |  Métodos:
     |  - cadastrar_exame(exame)
     |  - listar_todos_exames()
     |  - filtrar_exames(...)
     |  - remover_exame(id_exame)
     |  - atualizar_exame(...)
     |  - exportar_excel(...)
     |  - exportar_txt(...)
     |
     |  Methods defined here:
     |
     |  atualizar_exame(self, id_exame, nome_exame, is_interno, valor_exame)
     |      Atualiza um exame e retorna a representação simplificada.
     |
     |      Returns:
     |          dict: exame atualizado.
     |
     |  cadastrar_exame(self, exame: model.exame.Exame)
     |      Persiste um novo exame.
     |
     |      Args:
     |          exame (Exame)
     |
     |  exportar_excel(
     |      self,
     |      id_exame: int,
     |      nome_exame: str,
     |      is_interno: bool,
     |      min_valor: float,
     |      max_valor: float
     |  )
     |      Gera um arquivo Excel (BytesIO) com os exames filtrados.
     |
     |      Args:
     |          mesmos filtros de filtrar_exames
     |
     |      Returns:
     |          BytesIO: arquivo Excel pronto para envio via Flask send_file.
     |
     |  exportar_txt(
     |      self,
     |      id_exame: int,
     |      nome_exame: str,
     |      is_interno: bool,
     |      min_valor: float,
     |      max_valor: float
     |  )
     |      Gera um arquivo TXT (tab-separated) com os exames filtrados.
     |
     |      Returns:
     |          BytesIO: fluxo pronto para envio.
     |
     |  filtrar_exames(
     |      self,
     |      id_exame: int,
     |      nome_exame: str,
     |      is_interno: bool,
     |      min_valor: float,
     |      max_valor: float,
     |      por_pagina=50,
     |      pagina: int = 1,
     |      order_by: str = 'nome_cliente',
     |      order_dir: str = 'desc'
     |  )
     |      Filtra exames delegando ao repositório e formata o resultado.
     |
     |      Args:
     |          id_exame, nome_exame, is_interno, min_valor, max_valor: filtros.
     |          por_pagina (int|None): itens por página (None = sem paginação).
     |          pagina (int): página atual.
     |          order_by (str), order_dir (str): ordenação.
     |
     |      Returns:
     |          dict: {'exames': [...], 'total': int, 'total_filtrado': int}
     |
     |  listar_todos_exames(self)
     |      Retorna todos os exames no formato JSON serializável.
     |
     |      Returns:
     |          list[dict]: lista de exames.
     |
     |  remover_exame(self, id_exame)
     |      Remove exame por id.
     |
     |      Args:
     |          id_exame (int)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  repositorio = <repository.exame_repository.ExameRepository object>

FILE
    c:\users\rafae\desktop\orac-medseg\services\exame_service.py



---

## Módulo: routes.exame_routes

Python Library Documentation: module routes.exame_routes in routes

NAME
    routes.exame_routes - Módulo routes.exame_routes

DESCRIPTION
    Define rotas Flask para operações relacionadas a exames:
    - cadastro, listagem, filtragem, remoção, atualização,
    - exportação para XLS e TXT.

    Cada rota usa os decoradores de autenticação/autorização do módulo auxiliar.auxiliar.

FUNCTIONS
    atualizar_exame()
        Rota PUT para atualizar exame. Requer papel administrador ou gestor.

        Corpo JSON aceita:
        { "id_exame": int, "nome_exame": str, "is_interno": bool, "valor_exame": float }

    cadastrar_exame()
        Rota POST para cadastrar um exame.

        Corpo JSON esperado:
        {
          "nome_exame": str,
          "is_interno": bool,
          "valor_exame": float | str
        }

        Retorna:
            201 em sucesso, 400 em erro.

    exportar_excel()
        Rota POST que gera e envia um arquivo .xlsx com exames filtrados.

        Retorna:
            Arquivo para download com mimetype apropriado.

    exportar_txt()
        Rota POST que gera e envia um arquivo .txt (tab separated) com exames filtrados.

    filtrar_exame()
        Rota POST para filtrar exames com paginação e ordenação.

        Corpo JSON aceita chaves de filtro:
        id_exame, nome_exame, is_interno, min_valor, max_valor, pagina, por_pagina, order_by, order_dir

    listar_todos_exames()
        Rota GET para listar todos os exames.

        Retorna:
            JSON com lista de exames e código 200.

    remover_exame()
        Rota DELETE para remover exame. Requer papel administrador ou gestor.

        Corpo JSON:
        { "id_exame": int }

DATA
    exame_bp = <Blueprint 'exame'>
    request = <LocalProxy unbound>
    service = <services.exame_service.ExameService object>

FILE
    c:\users\rafae\desktop\orac-medseg\routes\exame_routes.py



---

## Módulo: model.usuario

Python Library Documentation: module model.usuario in model

NAME
    model.usuario - Módulo model.usuario

DESCRIPTION
    Define o modelo SQLAlchemy Usuario e operações simples relacionadas à senha.

CLASSES
    sqlalchemy.orm.decl_api.Base(builtins.object)
        Usuario

    class Usuario(sqlalchemy.orm.decl_api.Base)
     |  Usuario(**kwargs)
     |
     |  Modelo SQLAlchemy para a tabela 'usuario'.
     |
     |  Atributos:
     |  - id_usuario (int): chave primária autoincrement.
     |  - nome_usuario (str): nome do usuário.
     |  - email_usuario (str): email único e obrigatório.
     |  - senha (str): hash da senha.
     |  - role (Enum): papel do usuário (TiposUsuario).
     |  - foto_url (str|None): URL da foto armazenada externamente.
     |
     |  Métodos:
     |  - setar_senha(senha): armazena hash da senha.
     |  - checkar_senha(senha): verifica senha em relação ao hash.
     |
     |  Method resolution order:
     |      Usuario
     |      sqlalchemy.orm.decl_api.Base
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs) from sqlalchemy.orm.instrumentation
     |      A simple constructor that allows initialization from kwargs.
     |
     |      Sets attributes on the constructed instance using the names and
     |      values in ``kwargs``.
     |
     |      Only keys that are present as
     |      attributes of the instance's class are allowed. These could be,
     |      for example, any mapped columns or relationships.
     |
     |  checkar_senha(self, senha)
     |      Verifica se a senha fornecida corresponde ao hash armazenado.
     |
     |      Args:
     |          senha (str)
     |
     |      Returns:
     |          bool
     |
     |  setar_senha(self, senha)
     |      Gera e define o hash da senha para o usuário.
     |
     |      Args:
     |          senha (str)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  email_usuario
     |
     |  foto_url
     |
     |  id_usuario
     |
     |  nome_usuario
     |
     |  role
     |
     |  senha
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  __mapper__ = <Mapper at 0x2b102229950; Usuario>
     |
     |  __table__ = Table('usuario', MetaData(), Column('id_usuario'...tring(l...
     |
     |  __tablename__ = 'usuario'
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __abstract__ = True
     |
     |  metadata = MetaData()
     |
     |  registry = <sqlalchemy.orm.decl_api.registry object>

FILE
    c:\users\rafae\desktop\orac-medseg\model\usuario.py



---

## Módulo: repository.usuario_repository

Python Library Documentation: module repository.usuario_repository in repository

NAME
    repository.usuario_repository - Módulo repository.usuario_repository

DESCRIPTION
    Fornece UsuarioRepository para operações de persistência e consulta
    da entidade Usuario usando SQLAlchemy.

    Classes:
    - UsuarioRepository: métodos para salvar, listar, filtrar, buscar por id/email e remover usuários.

CLASSES
    builtins.object
        UsuarioRepository

    class UsuarioRepository(builtins.object)
     |  Repositório responsável pelo acesso a dados da entidade Usuario.
     |
     |  Atributos:
     |  - session: sessão do SQLAlchemy a ser usada para operações.
     |
     |  Métodos principais:
     |  - salvar(usuario): persiste ou atualiza um usuário.
     |  - listar_todos_usuarios(): retorna todos os usuários.
     |  - filtrar_usuarios(...): filtra usuários com paginação/ordenação.
     |  - filtrar_por_id(id_usuario): busca usuário por id.
     |  - filtrar_por_email(email_usuario): busca usuário por email.
     |  - remover_usuario(usuario_a_remover): remove usuário passado.
     |
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  filtrar_por_email(self, email_usuario)
     |      Busca um usuário pelo email.
     |
     |      Args:
     |          email_usuario (str)
     |
     |      Returns:
     |          Usuario|None: instância encontrada ou None.
     |
     |  filtrar_por_id(self, id_usuario)
     |      Busca um usuário pelo id.
     |
     |      Args:
     |          id_usuario (int)
     |
     |      Returns:
     |          Usuario|None: instância encontrada ou None.
     |
     |  filtrar_usuarios(
     |      self,
     |      id_usuario=None,
     |      nome_usuario=None,
     |      email_usuario=None,
     |      role=None,
     |      offset=None,
     |      limit=None,
     |      order_by=None,
     |      order_dir=None
     |  )
     |      Filtra usuários por vários critérios, com paginação e ordenação.
     |
     |      Args:
     |          id_usuario (int|None): filtro por id.
     |          nome_usuario (str|None): filtro por nome (like, case-insensitive).
     |          email_usuario (str|None): filtro por email (like).
     |          role (str|None): filtro por papel.
     |          offset (int|None), limit (int|None): paginação.
     |          order_by (str|None), order_dir (str|None): ordenação.
     |
     |      Returns:
     |          tuple: (resultados, total, total_filtrado)
     |
     |  listar_todos_usuarios(self)
     |      Retorna todos os usuários da base.
     |
     |      Returns:
     |          list[Usuario]: lista de instâncias Usuario.
     |
     |  remover_usuario(self, usuario_a_remover)
     |      Remove o usuário fornecido da sessão e confirma a transação.
     |
     |      Args:
     |          usuario_a_remover (Usuario)
     |
     |      Levanta:
     |          Exception em caso de erro.
     |
     |  salvar(self, usuario: model.usuario.Usuario)
     |      Persiste um usuário (insert ou update).
     |
     |      Args:
     |          usuario (Usuario): instância a ser salva.
     |
     |      Levanta:
     |          Exception em caso de erro; faz rollback antes de propagar.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

DATA
    Session = <sqlalchemy.orm.scoping.scoped_session object>
    func = <sqlalchemy.sql.functions._FunctionGenerator object>

FILE
    c:\users\rafae\desktop\orac-medseg\repository\usuario_repository.py



---

## Módulo: services.usuario_service

Python Library Documentation: module services.usuario_service in services

NAME
    services.usuario_service - Módulo services.usuario_service

DESCRIPTION
    Camada de serviço para operações de negócio relacionadas a Usuario:
    - validações básicas (ex.: email duplicado),
    - manipulação de foto via Google Drive,
    - geração e reset de senha,
    - exportação para Excel e TXT.

CLASSES
    builtins.object
        UsuarioService

    class UsuarioService(builtins.object)
     |  Serviço de alto nível para gerenciar usuários.
     |
     |  Atributos:
     |  - repositorio: instância de UsuarioRepository.
     |
     |  Métodos principais:
     |  - verificar_usuario(email, senha): autenticação básica.
     |  - cadastrar_usuario(...): cria usuário e envia foto ao Drive.
     |  - listar_todos_usuarios(): retorna usuários em JSON serializável.
     |  - filtrar_usuarios(...): filtragem com paginação/ordenação.
     |  - remover_usuario(id_usuario): remove usuário e exclui foto do Drive.
     |  - atualizar_usuario(...): atualiza campos e foto.
     |  - gerar_senha(), resetar_senha(email): utilitários para senhas.
     |  - exportar_excel(...), exportar_txt(...): geram arquivos para download.
     |
     |  Methods defined here:
     |
     |  atualizar_usuario(
     |      self,
     |      id_usuario,
     |      nome_usuario,
     |      email_usuario,
     |      senha,
     |      role,
     |      foto
     |  )
     |      Atualiza campos de um usuário (nome, email, senha, role e foto).
     |
     |      Faz upload da nova foto para o Drive e remove a anterior se necessário.
     |
     |      Returns:
     |          dict: representação serializável do usuário atualizado.
     |
     |  cadastrar_usuario(
     |      self,
     |      nome_usuario: str,
     |      email_usuario: str,
     |      role: enums.tipos_usuario.TiposUsuario,
     |      senha: str,
     |      foto=None
     |  )
     |      Registra um novo usuário, faz upload da foto se fornecida e retorna representação serializável.
     |
     |      Args:
     |          nome_usuario (str), email_usuario (str), role (TiposUsuario), senha (str), foto (FileStorage|None)
     |
     |      Returns:
     |          dict: dados do usuário criado ou dict com chave "erro" em caso de conflito.
     |
     |  exportar_excel(
     |      self,
     |      id_usuario: int,
     |      nome_usuario: str,
     |      email_usuario: str,
     |      role: enums.tipos_usuario.TiposUsuario
     |  )
     |      Gera um BytesIO contendo um Excel com os usuários filtrados.
     |
     |      Returns:
     |          BytesIO
     |
     |  exportar_txt(
     |      self,
     |      id_usuario: int,
     |      nome_usuario: str,
     |      email_usuario: str,
     |      role: enums.tipos_usuario.TiposUsuario
     |  )
     |      Gera um BytesIO contendo um TXT (tab-separated) com os usuários filtrados.
     |
     |      Returns:
     |          BytesIO
     |
     |  filtrar_usuarios(
     |      self,
     |      id_usuario: int,
     |      nome_usuario: str,
     |      email_usuario: str,
     |      role: enums.tipos_usuario.TiposUsuario,
     |      por_pagina=50,
     |      pagina: int = 1,
     |      order_by: str = 'nome_usuario',
     |      order_dir: str = 'desc'
     |  )
     |      Filtra usuários delegando ao repositório e formata o resultado.
     |
     |      Args:
     |          mesmos filtros de repository.filtrar_usuarios mais paginação e ordenação.
     |
     |      Returns:
     |          dict: {'usuarios': [...], 'total': int, 'total_filtrado': int}
     |
     |  gerar_senha(self)
     |      Gera uma senha aleatória contendo maiúsculas, minúsculas, números e caracteres especiais.
     |
     |      Returns:
     |          str: nova senha gerada.
     |
     |  listar_todos_usuarios(self)
     |      Retorna lista de todos os usuários em formato JSON serializável.
     |
     |      Returns:
     |          list[dict]
     |
     |  remover_usuario(self, id_usuario)
     |      Remove um usuário por id, removendo sua foto do Drive quando existir.
     |
     |      Args:
     |          id_usuario (int)
     |
     |  resetar_senha(self, email_usuario: str)
     |      Reseta a senha de um usuário e envia a nova senha por email.
     |
     |      Args:
     |          email_usuario (str)
     |
     |      Returns:
     |          bool|str: resultado do envio de email (depende da implementação do enviar()).
     |
     |  verificar_usuario(self, email_usuario: str, senha: str)
     |      Valida credenciais e retorna a instância do usuário ou None.
     |
     |      Args:
     |          email_usuario (str), senha (str)
     |
     |      Returns:
     |          Usuario|None
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  repositorio = <repository.usuario_repository.UsuarioRepository object>

FILE
    c:\users\rafae\desktop\orac-medseg\services\usuario_service.py



---

## Módulo: routes.usuario_routes

Python Library Documentation: module routes.usuario_routes in routes

NAME
    routes.usuario_routes - Módulo routes.usuario_routes

DESCRIPTION
    Define rotas Flask relacionadas à autenticação e gestão de usuários:
    - login, logout, reset de senha,
    - cadastro, listagem, filtragem, remoção e atualização de usuários,
    - exportação para XLS e TXT.

    Cada rota usa os decoradores de autenticação/autorização do módulo auxiliar.auxiliar.

FUNCTIONS
    atualizar_conta()
        Rota PUT para atualização da própria conta do usuário autenticado.

        Valida que o id fornecido corresponde ao usuário em sessão.

    atualizar_usuario()
        Rota PUT para atualização de usuário (administrador).

        Espera formulário multipart com campos atualizáveis:
        id_usuario, nome_usuario, email_usuario, senha, role, foto

        Retorna:
            200 com dados atualizados ou 400 em erro.

    cadastrar_usuario()
        Rota POST para cadastro de usuário.

        Espera formulário multipart com campos:
        nome_usuario, email_usuario, senha, role e opcionalmente foto.

        Retorna:
            201 com dados do usuário criado, 400 em erro ou conflito de email.

    exportar_excel()
        Rota POST que gera e envia um arquivo .xlsx com usuários filtrados.

    exportar_txt()
        Rota POST que gera e envia um arquivo .txt (tab separated) com usuários filtrados.

    filtrar_usuario()
        Rota POST para filtragem de usuários.

        Corpo JSON aceita filtros e paginação:
        id_usuario, nome_usuario, email_usuario, role, pagina, por_pagina, order_by, order_dir

    listar_todos_usuarios()
        Rota GET que retorna todos os usuários.

        Retorna:
            200 com lista de usuários em JSON, 400 em erro.

    login()
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

    logout()
        Rota POST para encerrar a sessão do usuário autenticado.

        Retorna:
            200 em sucesso, 400 em erro.

    remover_usuario()
        Rota DELETE para remoção de usuário por id.

        Corpo JSON esperado:
        { "id_usuario": int }

        Restrições:
        - um usuário não pode remover sua própria conta (retorna 403).
        - requer papel administrador.

    resetar_senha()
        Rota POST para reset de senha.

        Corpo JSON esperado:
        { "email_usuario": str }

        Retorna:
            200 com mensagem de envio em caso de sucesso,
            400 em erro.

DATA
    request = <LocalProxy unbound>
    service = <services.usuario_service.UsuarioService object>
    session = <LocalProxy unbound>
    usuario_bp = <Blueprint 'usuario'>

FILE
    c:\users\rafae\desktop\orac-medseg\routes\usuario_routes.py



---

## Módulo: services.google_services.google_service

Python Library Documentation: module services.google_services.google_service in services.google_services

NAME
    services.google_services.google_service - Módulo services.google_services.google_service

DESCRIPTION
    Fornece utilitário para autenticação com a API do Google Drive usando
    uma conta de serviço e delegação para um usuário (SERVICE_ACCOUNT_FILE,
    EMAIL_USER e SCOPES devem estar definidos no .env).

    Funções:
    - acessando_drive(): retorna uma instância do serviço Drive v3 autenticada.

FUNCTIONS
    acessando_drive()
        Cria e retorna o objeto de serviço do Google Drive (v3).

        Lê SERVICE_ACCOUNT_FILE, EMAIL_USER e SCOPES do ambiente, carrega as
        credenciais da conta de serviço e delega para EMAIL_USER.

        Returns:
            googleapiclient.discovery.Resource: cliente para interagir com o Drive.

FILE
    c:\users\rafae\desktop\orac-medseg\services\google_services\google_service.py



---

## Módulo: services.google_services.envio_email

Python Library Documentation: module services.google_services.envio_email in services.google_services

NAME
    services.google_services.envio_email - Módulo services.google_services.envio_email

DESCRIPTION
    Helpers para criação e envio de emails via Gmail API usando credenciais de
    conta de serviço delegada. Depende das variáveis de ambiente:
    SERVICE_ACCOUNT_FILE, SCOPES_EMAIL, EMAIL_USER e TEMPLATE_PATH.

    Funções:
    - carregar_template(nome_usuario, nova_senha): carrega e substitui placeholders no template HTML.
    - criar_email(email_usuario, nome_usuario, nova_senha): constrói a mensagem MIME e retorna o payload pronto.
    - enviar(email_usuario, nome_usuario, nova_senha): envia o email usando a API Gmail.

FUNCTIONS
    carregar_template(nome_usuario, nova_senha)
        Lê o arquivo de template HTML e substitui os placeholders.

        Args:
            nome_usuario (str): nome do destinatário.
            nova_senha (str): senha a ser inserida no template.

        Returns:
            str: HTML com valores preenchidos.

    criar_email(email_usuario, nome_usuario, nova_senha)
        Monta a mensagem MIME multipart com o template carregado e retorna
        o objeto compatível com a API Gmail (raw base64-url-safe).

        Args:
            email_usuario (str)
            nome_usuario (str)
            nova_senha (str)

        Returns:
            dict: payload {'raw': ...} pronto para envio via service.users().messages().send(...)

    enviar(email_usuario, nome_usuario, nova_senha)
        Envia o email montado pela função criar_email usando a API Gmail.

        Args:
            email_usuario (str)
            nome_usuario (str)
            nova_senha (str)

        Returns:
            str: email do destinatário (usado como confirmação).

DATA
    EMAIL_USER = 'inov2@controller-oraculus.com.br'
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    SERVICE_ACCOUNT_FILE = r'C:\Users\rafae\Desktop\orac-medseg\services\g...
    TEMPLATE_PATH = 'email/Esqueceu a senha.html'
    base_dir = r'C:\Users\rafae\Desktop\orac-medseg\services\google_servic...
    credentials = <google.oauth2.service_account.Credentials object>
    credentials_filename = 'credentials.json'
    service = <googleapiclient.discovery.Resource object>

FILE
    c:\users\rafae\desktop\orac-medseg\services\google_services\envio_email.py



---

## Módulo: services.google_services.envio_drive

Python Library Documentation: module services.google_services.envio_drive in services.google_services

NAME
    services.google_services.envio_drive - Módulo services.google_services.envio_drive

DESCRIPTION
    Funções utilitárias para upload e remoção de arquivos no Google Drive usando
    o serviço retornado por services.google_services.google_service.acessando_drive.

    Depende da variável de ambiente PASTA_DRIVE_FOTOS (PASTA_RAIZ_ID).
    Funções:
    - salvar_drive(nome_arquivo, email_usuario, nome_usuario): faz upload e retorna id do arquivo.
    - remover_drive(id_arquivo): remove arquivo pelo id.

FUNCTIONS
    remover_drive(id_arquivo)
        Remove um arquivo do Drive pelo seu id.

        Args:
            id_arquivo (str)

        Returns:
            bool: True se a operação foi executada (lança exceção em caso de erro).

    salvar_drive(nome_arquivo, email_usuario, nome_usuario)
        Faz upload de um arquivo local para a pasta especificada no Drive.

        Args:
            nome_arquivo (str): caminho local do arquivo a enviar.
            email_usuario (str): usado para compor o nome do arquivo no Drive.
            nome_usuario (str): usado para compor o nome do arquivo no Drive.

        Returns:
            str: id do arquivo criado no Drive.

DATA
    PASTA_RAIZ_ID = '1esuyPFdEy-2RlZaE0cwgarbRzeameDCX'

FILE
    c:\users\rafae\desktop\orac-medseg\services\google_services\envio_drive.py



---

## Módulo: model.cliente

Python Library Documentation: module model.cliente in model

NAME
    model.cliente - Módulo model.cliente

DESCRIPTION
    Define a entidade Cliente e a tabela associativa cliente_exame.

CLASSES
    sqlalchemy.orm.decl_api.Base(builtins.object)
        Cliente

    class Cliente(sqlalchemy.orm.decl_api.Base)
     |  Cliente(**kwargs)
     |
     |  Modelo SQLAlchemy para a tabela 'cliente'.
     |
     |  Atributos de coluna:
     |  - id_cliente (int): chave primária autoincrement.
     |  - nome_cliente (str): nome do cliente.
     |  - cnpj_cliente (str): CNPJ sem formatação.
     |  - tipo_cliente (Enum): valor do enum TiposCliente.
     |  - exames_incluidos (list[Exame]): relação many-to-many com Exame via cliente_exame.
     |
     |  Method resolution order:
     |      Cliente
     |      sqlalchemy.orm.decl_api.Base
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs) from sqlalchemy.orm.instrumentation
     |      A simple constructor that allows initialization from kwargs.
     |
     |      Sets attributes on the constructed instance using the names and
     |      values in ``kwargs``.
     |
     |      Only keys that are present as
     |      attributes of the instance's class are allowed. These could be,
     |      for example, any mapped columns or relationships.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  cnpj_cliente
     |
     |  exames_incluidos
     |
     |  id_cliente
     |
     |  nome_cliente
     |
     |  tipo_cliente
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  __mapper__ = <Mapper at 0x2b10202bc50; Cliente>
     |
     |  __table__ = Table('cliente', MetaData(), Column('id_cliente'...e='tipo...
     |
     |  __tablename__ = 'cliente'
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __abstract__ = True
     |
     |  metadata = MetaData()
     |
     |  registry = <sqlalchemy.orm.decl_api.registry object>

DATA
    cliente_exame = Table('cliente_exame', MetaData(), Column('id_cl..., p...

FILE
    c:\users\rafae\desktop\orac-medseg\model\cliente.py



---

## Módulo: repository.cliente_repository

Python Library Documentation: module repository.cliente_repository in repository

NAME
    repository.cliente_repository - Módulo repository.cliente_repository

DESCRIPTION
    Fornece a classe ClienteRepository para operações CRUD e de filtragem
    sobre a entidade Cliente usando SQLAlchemy.

    Classes:
    - ClienteRepository: métodos para adicionar, listar, filtrar, atualizar e remover clientes.

CLASSES
    builtins.object
        ClienteRepository

    class ClienteRepository(builtins.object)
     |  Repositório responsável pelo acesso a dados da entidade Cliente.
     |
     |  Atributos:
     |  - session: sessão do SQLAlchemy a ser usada para operações.
     |
     |  Métodos principais:
     |  - adicionar_cliente(cliente): persiste um novo cliente.
     |  - listar_todos_clientes(): retorna todos os clientes com exames carregados.
     |  - filtrar_clientes(...): filtra clientes por vários campos, ordenação e paginação.
     |  - filtrar_por_id(id_cliente): retorna um cliente por id.
     |  - filtrar_por_cnpj(cnpj_cliente): retorna um cliente por CNPJ.
     |  - remover_cliente(id_cliente): remove cliente por id.
     |  - atualizar_cliente(...): atualiza campos do cliente e relacionamentos.
     |
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  adicionar_cliente(self, cliente: model.cliente.Cliente)
     |      Adiciona um novo cliente ao banco.
     |
     |      Args:
     |          cliente (Cliente): instância de Cliente a ser persistida.
     |
     |      Levanta:
     |          Exception em caso de erro; faz rollback antes de propagar.
     |
     |  atualizar_cliente(
     |      self,
     |      id_cliente,
     |      nome_cliente,
     |      cnpj_cliente,
     |      tipo_cliente,
     |      exames_incluidos
     |  )
     |      Atualiza campos de um cliente existente.
     |
     |      Args:
     |          id_cliente (int): id do cliente a atualizar.
     |          nome_cliente (str|None): novo nome (se fornecido).
     |          cnpj_cliente (str|None): novo CNPJ (se fornecido).
     |          tipo_cliente (TiposCliente|None): novo tipo (se fornecido).
     |          exames_incluidos (list[Exame]|None): lista de exames relacionados (substitui a lista atual).
     |
     |      Returns:
     |          dict: representação simplificada do cliente atualizado.
     |
     |  filtrar_clientes(
     |      self,
     |      id_cliente=None,
     |      nome_cliente=None,
     |      cnpj_cliente=None,
     |      tipo_cliente=None,
     |      exames_incluidos=None,
     |      offset=None,
     |      limit=None,
     |      order_by=None,
     |      order_dir=None
     |  )
     |      Filtra clientes por diversos critérios, com suporte a paginação e ordenação.
     |
     |      Args:
     |          id_cliente (int|None): filtro por id.
     |          nome_cliente (str|None): filtro por nome (like, case-insensitive).
     |          cnpj_cliente (str|None): filtro por CNPJ (like, case-insensitive).
     |          tipo_cliente (list|None): lista de TiposCliente para filtrar.
     |          exames_incluidos (list[int]|None): lista de ids de exames; retorna clientes que possuem esses exames.
     |          offset (int|None): deslocamento para paginação.
     |          limit (int|None): limite de resultados.
     |          order_by (str|None): campo para ordenação.
     |          order_dir (str|None): 'asc' ou 'desc'.
     |
     |      Returns:
     |          tuple: (resultados, total, total_filtrado)
     |              - resultados: lista de clientes filtrados.
     |              - total: total de clientes na tabela antes do filtro.
     |              - total_filtrado: total de clientes após aplicação dos filtros.
     |
     |  filtrar_por_cnpj(self, cnpj_cliente)
     |      Retorna o cliente correspondente ao CNPJ fornecido.
     |
     |      Args:
     |          cnpj_cliente (str): CNPJ do cliente.
     |
     |      Returns:
     |          Cliente|None: instância Cliente ou None se não encontrado.
     |
     |  filtrar_por_id(self, id_cliente)
     |      Retorna o cliente correspondente ao id fornecido, carregando exames.
     |
     |      Args:
     |          id_cliente (int): id do cliente.
     |
     |      Returns:
     |          Cliente|None: instância Cliente ou None se não encontrado.
     |
     |  listar_todos_clientes(self)
     |      Lista todos os clientes, incluindo exames relacionados.
     |
     |      Returns:
     |          list[Cliente]: lista de instâncias Cliente.
     |
     |  remover_cliente(self, id_cliente)
     |      Remove o cliente com o id informado.
     |
     |      Args:
     |          id_cliente (int): id do cliente a remover.
     |
     |      Levanta:
     |          Exception em caso de erro.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

DATA
    Session = <sqlalchemy.orm.scoping.scoped_session object>
    func = <sqlalchemy.sql.functions._FunctionGenerator object>

FILE
    c:\users\rafae\desktop\orac-medseg\repository\cliente_repository.py



---

## Módulo: services.cliente_service

Python Library Documentation: module services.cliente_service in services

NAME
    services.cliente_service - Módulo services.cliente_service

DESCRIPTION
    Contém a camada de serviço para operações de negócio relacionadas a Cliente:
    - validações simples (ex.: CNPJ duplicado),
    - transformação de modelos para JSON,
    - exportação para Excel e TXT,
    - integração com serviço externo para consulta de nome por CNPJ.

CLASSES
    builtins.object
        ClienteService

    class ClienteService(builtins.object)
     |  Serviço de alto nível para gerenciar clientes.
     |
     |  Atributos:
     |  - repositorio: instância de ClienteRepository.
     |  - repositorio_exame: instância de ExameRepository.
     |
     |  Métodos expostos:
     |  - cadastrar_cliente(...)
     |  - listar_todos_clientes()
     |  - filtrar_clientes(...)
     |  - remover_cliente(id_cliente)
     |  - atualizar_cliente(...)
     |  - buscar_cnpj(cnpj)
     |  - exportar_excel(...)
     |  - exportar_txt(...)
     |
     |  Methods defined here:
     |
     |  atualizar_cliente(
     |      self,
     |      id_cliente: int,
     |      nome_cliente: str,
     |      cnpj_cliente: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      exames_incluidos: list[int]
     |  )
     |      Atualiza um cliente existente e retorna sua representação JSON.
     |
     |      Verifica duplicidade de CNPJ antes de persistir.
     |
     |      Returns:
     |          dict: cliente atualizado em formato serializável ou dict {'erro': ...}.
     |
     |  buscar_cnpj(self, cnpj: str)
     |      Consulta um serviço externo (receitaws) para recuperar o nome da empresa pelo CNPJ.
     |
     |      Args:
     |          cnpj (str)
     |
     |      Returns:
     |          str|None: nome retornado pela API ou None se indisponível.
     |
     |  cadastrar_cliente(
     |      self,
     |      nome_cliente: str,
     |      cnpj_cliente: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      exames_incluidos: list[int]
     |  )
     |      Registra um novo cliente após validação de CNPJ duplicado.
     |
     |      Args:
     |          nome_cliente (str)
     |          cnpj_cliente (str)
     |          tipo_cliente (TiposCliente)
     |          exames_incluidos (list[int]): lista de ids de exames.
     |
     |      Returns:
     |          dict|None: dicionário com erro quando houver CNPJ duplicado, caso contrário None.
     |
     |  exportar_excel(
     |      self,
     |      id_cliente: int,
     |      nome_cliente: str,
     |      cnpj_cliente: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      exames_incluidos: list[int]
     |  )
     |      Gera um arquivo Excel (BytesIO) com os clientes filtrados.
     |
     |      Args:
     |          mesmos filtros de filtrar_clientes
     |
     |      Returns:
     |          BytesIO: arquivo Excel pronto para envio via Flask send_file.
     |
     |  exportar_txt(
     |      self,
     |      id_cliente: int,
     |      nome_cliente: str,
     |      cnpj_cliente: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      exames_incluidos: list[int]
     |  )
     |      Gera um arquivo TXT (tab-separated) com os clientes filtrados.
     |
     |      Returns:
     |          BytesIO: fluxo pronto para envio.
     |
     |  filtrar_clientes(
     |      self,
     |      id_cliente: int,
     |      nome_cliente: str,
     |      cnpj_cliente: str,
     |      tipo_cliente: list[enums.tipos_cliente.TiposCliente],
     |      exames_incluidos: list[int],
     |      por_pagina=50,
     |      pagina: int = 1,
     |      order_by: str = 'nome_cliente',
     |      order_dir: str = 'desc'
     |  )
     |      Realiza a filtragem de clientes delegando ao repositório e formatando o resultado.
     |
     |      Args:
     |          id_cliente, nome_cliente, cnpj_cliente, tipo_cliente, exames_incluidos: filtros.
     |          por_pagina (int|None): quantos itens por página (None para sem paginação).
     |          pagina (int): página atual.
     |          order_by (str), order_dir (str): ordenação.
     |
     |      Returns:
     |          dict: {'clientes': [...], 'total': int, 'total_filtrado': int}
     |
     |  listar_todos_clientes(self)
     |      Retorna todos os clientes formatados em JSON serializável.
     |
     |      Returns:
     |          list[dict]: lista de clientes com seus exames no formato dicionário.
     |
     |  remover_cliente(self, id_cliente)
     |      Remove cliente por id.
     |
     |      Args:
     |          id_cliente (int)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  repositorio = <repository.cliente_repository.ClienteRepository object>
     |
     |  repositorio_exame = <repository.exame_repository.ExameRepository objec...

FILE
    c:\users\rafae\desktop\orac-medseg\services\cliente_service.py



---

## Módulo: routes.cliente_routes

Python Library Documentation: module routes.cliente_routes in routes

NAME
    routes.cliente_routes - Módulo routes.cliente_routes

DESCRIPTION
    Define rotas Flask para operações relacionadas a clientes:
    - cadastro, listagem, filtragem, remoção, atualização,
    - busca de CNPJ via serviço externo,
    - exportação para XLS e TXT.
    Cada rota utiliza decoradores de autenticação/autorização definidos em auxiliar.auxiliar.

FUNCTIONS
    atualizar_cliente()
        Rota PUT para atualizar cliente. Requer papel administrador ou gestor.

        Corpo JSON aceita os mesmos campos do cadastro.

    buscar_cnpj()
        Rota POST que retorna o nome associado a um CNPJ usando serviço externo.

        Corpo JSON:
        { "cnpj": str }

    cadastrar_cliente()
        Rota POST para cadastrar um cliente.

        Corpo JSON esperado:
        {
          "nome_cliente": str,
          "cnpj_cliente": str,
          "tipo_cliente": str,
          "exames_incluidos": [int]
        }

        Retorna:
            201 em sucesso, 400 em erro ou CNPJ duplicado.

    exportar_excel()
        Rota POST que gera e envia um arquivo .xlsx com clientes filtrados.

        Retorna:
            Arquivo para download com mimetype apropriado.

    exportar_txt()
        Rota POST que gera e envia um arquivo .txt (tab separated) com clientes filtrados.

    filtrar_clientes()
        Rota POST para filtrar clientes com paginação e ordenação.

        Corpo JSON aceita chaves de filtro e paginação.

    listar_todos_clientes()
        Rota GET para listar todos os clientes.

        Retorna:
            JSON com lista de clientes e código 200.

    remover_cliente()
        Rota DELETE para remover cliente. Requer papel administrador ou gestor.

        Corpo JSON:
        { "id_cliente": int }

DATA
    cliente_bp = <Blueprint 'cliente'>
    request = <LocalProxy unbound>
    service = <services.cliente_service.ClienteService object>

FILE
    c:\users\rafae\desktop\orac-medseg\routes\cliente_routes.py



---

## Módulo: model.atendimento

Python Library Documentation: module model.atendimento in model

NAME
    model.atendimento - Módulo model.atendimento

DESCRIPTION
    Define o modelo SQLAlchemy Atendimento e a tabela associativa atendimento_exame.

    Classe:
    - Atendimento: representa um atendimento realizado, relacionando-se a Cliente e Exame.

CLASSES
    sqlalchemy.orm.decl_api.Base(builtins.object)
        Atendimento

    class Atendimento(sqlalchemy.orm.decl_api.Base)
     |  Atendimento(**kwargs)
     |
     |  Modelo SQLAlchemy para a tabela 'atendimento'.
     |
     |  Atributos de coluna:
     |  - id_atendimento (int): chave primária autoincrement.
     |  - data_atendimento (datetime): data e hora do atendimento.
     |  - tipo_atendimento (Enum): valor do enum TiposAtendimento.
     |  - usuario (str): nome do atendente.
     |  - valor (float): valor cobrado pelo atendimento.
     |  - colaborador_atendimento (str): colaborador vinculado.
     |  - is_ativo (bool): status do atendimento.
     |  - id_cliente (int): FK para cliente.
     |  - cliente_atendimento (Cliente): relação many-to-one com Cliente.
     |  - exames_atendimento (list[Exame]): relação many-to-many com Exame via atendimento_exame.
     |
     |  Method resolution order:
     |      Atendimento
     |      sqlalchemy.orm.decl_api.Base
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, **kwargs) from sqlalchemy.orm.instrumentation
     |      A simple constructor that allows initialization from kwargs.
     |
     |      Sets attributes on the constructed instance using the names and
     |      values in ``kwargs``.
     |
     |      Only keys that are present as
     |      attributes of the instance's class are allowed. These could be,
     |      for example, any mapped columns or relationships.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  cliente_atendimento
     |
     |  colaborador_atendimento
     |
     |  data_atendimento
     |
     |  exames_atendimento
     |
     |  id_atendimento
     |
     |  id_cliente
     |
     |  is_ativo
     |
     |  tipo_atendimento
     |
     |  usuario
     |
     |  valor
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  __mapper__ = <Mapper at 0x2b1028cd6d0; Atendimento>
     |
     |  __table__ = Table('atendimento', MetaData(), Column('id_aten....id_cli...
     |
     |  __tablename__ = 'atendimento'
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from sqlalchemy.orm.decl_api.Base:
     |
     |  __abstract__ = True
     |
     |  metadata = MetaData()
     |
     |  registry = <sqlalchemy.orm.decl_api.registry object>

DATA
    atendimento_exame = Table('atendimento_exame', MetaData(), Column('i.....

FILE
    c:\users\rafae\desktop\orac-medseg\model\atendimento.py



---

## Módulo: repository.atendimento_repository

Python Library Documentation: module repository.atendimento_repository in repository

NAME
    repository.atendimento_repository - Módulo repository.atendimento_repository

DESCRIPTION
    Repositório para operações sobre a entidade Atendimento usando SQLAlchemy.

    Fornece métodos para:
    - adicionar, listar, filtrar, buscar por id, remover e atualizar atendimentos.

CLASSES
    builtins.object
        AtendimentoRepository

    class AtendimentoRepository(builtins.object)
     |  Repositório responsável pelo acesso a dados da entidade Atendimento.
     |
     |  Atributos:
     |  - session: sessão do SQLAlchemy a ser usada para operações.
     |
     |  Métodos:
     |  - adicionar_atendimento(atendimento)
     |  - listar_todos_atendimentos()
     |  - filtrar_atendimentos(...)
     |  - filtrar_por_id(id_atendimento)
     |  - remover_atendimento(id_atendimento)
     |  - atualizar_atendimento(...)
     |
     |  Methods defined here:
     |
     |  __init__(self)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  adicionar_atendimento(self, atendimento: model.atendimento.Atendimento)
     |      Persiste um novo atendimento na base.
     |
     |      Args:
     |          atendimento (Atendimento)
     |
     |  atualizar_atendimento(
     |      self,
     |      id_atendimento,
     |      data_atendimento,
     |      tipo_atendimento,
     |      usuario,
     |      valor,
     |      colaborador_atendimento,
     |      is_ativo,
     |      cliente_atendimento,
     |      exames_atendimento
     |  )
     |      Atualiza campos de um atendimento existente e salva a transação.
     |
     |      Args:
     |          id_atendimento (int), data_atendimento (str "DD/MM/YYYY"|None), tipo_atendimento, usuario,
     |          valor, colaborador_atendimento, is_ativo, cliente_atendimento (Cliente|None),
     |          exames_atendimento (list[Exame]|None)
     |
     |      Returns:
     |          dict: representação simplificada do atendimento atualizado.
     |
     |  filtrar_atendimentos(
     |      self,
     |      id_atendimento=None,
     |      min_data=None,
     |      max_data=None,
     |      tipo_atendimento=None,
     |      usuario=None,
     |      min_valor=None,
     |      max_valor=None,
     |      colaborador_atendimento=None,
     |      tipo_cliente=None,
     |      is_ativo=None,
     |      ids_clientes=None,
     |      ids_exames=None,
     |      offset=None,
     |      limit=None,
     |      order_by=None,
     |      order_dir=None
     |  )
     |      Filtra atendimentos por múltiplos critérios com paginação e ordenação.
     |
     |      Args:
     |          id_atendimento (int|None), min_data (str "YYYY-MM-DD"|None), max_data (str|None),
     |          tipo_atendimento (list|None), usuario (str|None), min_valor (float|None),
     |          max_valor (float|None), colaborador_atendimento (str|None), tipo_cliente (list|None),
     |          is_ativo (bool|None), ids_clientes (list[int]|None), ids_exames (list[int]|None),
     |          offset (int|None), limit (int|None), order_by (str|None), order_dir (str|None).
     |
     |      Returns:
     |          tuple: (resultados, total, total_filtrado, valor_total)
     |
     |  filtrar_por_id(self, id_atendimento)
     |      Retorna o atendimento correspondente ao id fornecido, carregando cliente e exames.
     |
     |      Args:
     |          id_atendimento (int)
     |
     |      Returns:
     |          Atendimento|None
     |
     |  listar_todos_atendimentos(self)
     |      Retorna todos os atendimentos com relacionamentos carregados.
     |
     |      Returns:
     |          list[Atendimento]
     |
     |  remover_atendimento(self, id_atendimento)
     |      Remove atendimento por id.
     |
     |      Args:
     |          id_atendimento (int)
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

DATA
    Session = <sqlalchemy.orm.scoping.scoped_session object>
    func = <sqlalchemy.sql.functions._FunctionGenerator object>

FILE
    c:\users\rafae\desktop\orac-medseg\repository\atendimento_repository.py



---

## Módulo: services.atendimento_service

Python Library Documentation: module services.atendimento_service in services

NAME
    services.atendimento_service - Módulo services.atendimento_service

DESCRIPTION
    Camada de serviço para operações de negócio relacionadas a Atendimentos:
    - cálculos de valores, validações simples,
    - transformação de modelos para JSON,
    - exportação para Excel e TXT.

    Responsável por orquestrar repositórios de Atendimento, Cliente e Exame.

CLASSES
    builtins.object
        AtendimentoService

    class AtendimentoService(builtins.object)
     |  Serviço de alto nível para gerenciar atendimentos.
     |
     |  Atributos:
     |  - repositorio: AtendimentoRepository
     |  - repositorio_cliente: ClienteRepository
     |  - repositorio_exame: ExameRepository
     |
     |  Métodos expostos:
     |  - cadastrar_atendimento(...)
     |  - listar_todos_atendimentos()
     |  - filtrar_atendimentos(...)
     |  - remover_atendimento(id_atendimento)
     |  - atualizar_atendimento(...)
     |  - exportar_excel(...)
     |  - exportar_txt(...)
     |
     |  Methods defined here:
     |
     |  atualizar_atendimento(
     |      self,
     |      id_atendimento,
     |      data_atendimento,
     |      tipo_atendimento,
     |      usuario,
     |      valor,
     |      colaborador_atendimento,
     |      is_ativo,
     |      id_cliente,
     |      ids_exames
     |  )
     |      Atualiza um atendimento, recalculando valores e relacionamentos quando necessário.
     |
     |      Retorna a representação JSON do atendimento atualizado.
     |
     |  cadastrar_atendimento(
     |      self,
     |      tipo_atendimento: enums.tipos_atendimento.TiposAtendimento,
     |      usuario: str,
     |      valor: float,
     |      colaborador_atendimento: str,
     |      id_cliente: int,
     |      ids_exames: list[int]
     |  )
     |      Cria e persiste um novo atendimento.
     |
     |      Calcula valor total com base em exames não incluídos no plano do cliente,
     |      usa data/hora atual e relaciona cliente e exames.
     |
     |  exportar_excel(
     |      self,
     |      id_atendimento: str,
     |      min_data: str,
     |      max_data: str,
     |      tipo_atendimento: enums.tipos_atendimento.TiposAtendimento,
     |      usuario: str,
     |      min_valor: float,
     |      max_valor: str,
     |      colaborador_atendimento: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      is_ativo: bool,
     |      ids_clientes: list[int],
     |      ids_exames: list[int]
     |  )
     |      Gera um BytesIO com um arquivo Excel contendo os atendimentos filtrados.
     |
     |  exportar_txt(
     |      self,
     |      id_atendimento: str,
     |      min_data: str,
     |      max_data: str,
     |      tipo_atendimento: enums.tipos_atendimento.TiposAtendimento,
     |      usuario: str,
     |      min_valor: float,
     |      max_valor: str,
     |      colaborador_atendimento: str,
     |      tipo_cliente: enums.tipos_cliente.TiposCliente,
     |      is_ativo: bool,
     |      ids_clientes: list[int],
     |      ids_exames: list[int]
     |  )
     |      Gera um BytesIO com um arquivo TXT (tab-separated) contendo os atendimentos filtrados.
     |
     |  filtrar_atendimentos(
     |      self,
     |      id_atendimento: str,
     |      min_data: str,
     |      max_data: str,
     |      tipo_atendimento: list[enums.tipos_atendimento.TiposAtendimento],
     |      usuario: str,
     |      min_valor: float,
     |      max_valor: str,
     |      colaborador_atendimento: str,
     |      tipo_cliente: list[enums.tipos_cliente.TiposCliente],
     |      is_ativo: bool,
     |      ids_clientes: list[int],
     |      ids_exames: list[int],
     |      pagina: int = 1,
     |      por_pagina=50,
     |      order_by: str = 'data_atendimento',
     |      order_dir: str = 'desc'
     |  )
     |      Filtra atendimentos delegando ao repositório e formata o resultado para a API.
     |
     |      Retorna um dicionário com total, total_filtrado, lista de atendimentos e valor_total.
     |
     |  listar_todos_atendimentos(self)
     |      Retorna todos os atendimentos formatados em JSON serializável.
     |
     |      Cada atendimento inclui dados do cliente e lista de exames.
     |
     |  remover_atendimento(self, id_atendimento)
     |      Remove atendimento por id (delegado ao repositório).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  repositorio = <repository.atendimento_repository.AtendimentoRepository...
     |
     |  repositorio_cliente = <repository.cliente_repository.ClienteRepository...
     |
     |  repositorio_exame = <repository.exame_repository.ExameRepository objec...

FILE
    c:\users\rafae\desktop\orac-medseg\services\atendimento_service.py



---

## Módulo: routes.atendimento_routes

Python Library Documentation: module routes.atendimento_routes in routes

NAME
    routes.atendimento_routes - Módulo routes.atendimento_routes

DESCRIPTION
    Define as rotas Flask para operações relacionadas a Atendimentos:
    - cadastro, listagem, filtragem, atualização,
    - exportação para XLS e TXT.

    Cada rota aplica decoradores de autenticação/autorização do módulo auxiliar.auxiliar.
    As rotas recebem e retornam JSON (exceto endpoints que retornam arquivos).

FUNCTIONS
    atualizar_atendimento()
        Rota PUT para atualizar um atendimento existente.

        Corpo JSON esperado:
        {
          "id_atendimento": int,
          "data_atendimento": "DD/MM/YYYY" | None,
          "tipo_atendimento": str | None,
          "valor": float | None,
          "colaborador_atendimento": str | None,
          "is_ativo": bool | None,
          "id_cliente": int | None,
          "ids_exames": [int] | None
        }

        Requer papel administrador ou gestor.

    cadastrar_atendimento()
        Rota POST para cadastrar um novo atendimento.

        Corpo JSON esperado:
        {
          "tipo_atendimento": str,
          "valor": float | None,
          "colaborador_atendimento": str,
          "id_cliente": int,
          "ids_exames": [int]
        }

        Retorna:
            201 em sucesso, 400 em erro.

    exportar_excel()
        Rota POST que gera e envia um arquivo .xlsx com atendimentos filtrados.

        Recebe filtro no corpo JSON em 'filtrosAtuais' e retorna o arquivo para download.

    exportar_txt()
        Rota POST que gera e envia um arquivo .txt (tab separated) com atendimentos filtrados.

        Recebe filtro no corpo JSON em 'filtrosAtuais' e retorna o arquivo para download.

    filtrar_atendimentos()
        Rota POST para filtrar atendimentos com paginação e ordenação.

        Corpo JSON aceita filtros:
        id_atendimento, min_data, max_data, tipo_atendimento, usuario, min_valor, max_valor,
        colaborador_atendimento, tipo_cliente, is_ativo, ids_clientes, ids_exames, pagina, por_pagina, order_by, order_dir

        Retorna:
            200 com resultados filtrados ou 400 em erro.

    listar_todos_atendimentos()
        Rota GET para listar todos os atendimentos.

        Retorna:
            200 com JSON contendo lista de atendimentos, 400 em erro.

DATA
    atendimento_bp = <Blueprint 'atendimento'>
    request = <LocalProxy unbound>
    service = <services.atendimento_service.AtendimentoService object>
    session = <LocalProxy unbound>

FILE
    c:\users\rafae\desktop\orac-medseg\routes\atendimento_routes.py


