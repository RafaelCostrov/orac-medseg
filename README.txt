ORAC MED

1) Pré‑requisitos
- Python 3.9+ instalado e disponível no PATH.
- Git (opcional).
- Conta Google e credenciais para integração Drive/e‑mail.

2) Criar e ativar ambiente virtual
- Criar:
  python -m venv .venv
- Ativar (CMD):
  .venv\Scripts\activate
- Ativar (PowerShell):
  .venv\Scripts\Activate.ps1

3) Atualizar pip e instalar dependências
- Atualizar pip:
  python -m pip install --upgrade pip
- Instalar requirements:
  pip install -r requirements.txt

4) Variáveis de ambiente / arquivo .env
- Criar arquivo .env na raiz do projeto (não comitar).
- Variáveis recomendadas:
  SENHA_BD (Senha do banco de dados)
  PASTA_DRIVE_FOTOS (Pasta do drive para armazenar as fotos dos usuários)
  SERVICE_ACCOUNT_FILE (credenciais para uso da API do Google)
  EMAIL_USER (Email utilizado na API)
  SCOPES_DRIVE (Escopo para utilizar o Google Drive)
  SCOPES_EMAIL (Escopo para utilizar o Gmail)
  TEMPLATE_PATH (Caminho para o template HTML do email)

5) Colocar credenciais do Google
- Copie/coloque o arquivo de credenciais em:
  services\google_services\credentials.json
- Confirme o caminho em .env.

6) Executar a aplicação
  python main.py

7) Acessar interface
- Abra no navegador:
  http://localhost:5000 (ou outra que tiver utilizando)
