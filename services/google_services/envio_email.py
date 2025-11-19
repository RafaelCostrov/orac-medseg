"""
Módulo services.google_services.envio_email

Helpers para criação e envio de emails via Gmail API usando credenciais de
conta de serviço delegada. Depende das variáveis de ambiente:
SERVICE_ACCOUNT_FILE, SCOPES_EMAIL, EMAIL_USER e TEMPLATE_PATH.

Funções:
- carregar_template(nome_usuario, nova_senha): carrega e substitui placeholders no template HTML.
- criar_email(email_usuario, nome_usuario, nova_senha): constrói a mensagem MIME e retorna o payload pronto.
- enviar(email_usuario, nome_usuario, nova_senha): envia o email usando a API Gmail.
"""
import os
import base64
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

load_dotenv()
base_dir = os.path.dirname(os.path.abspath(__file__))
credentials_filename = os.getenv("SERVICE_ACCOUNT_FILE")
SERVICE_ACCOUNT_FILE = os.path.join(base_dir, credentials_filename)
SCOPES = os.getenv('SCOPES_EMAIL').split(',')
EMAIL_USER = os.getenv('EMAIL_USER')
TEMPLATE_PATH = os.getenv('TEMPLATE_PATH')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
).with_subject(EMAIL_USER)
service = build('gmail', 'v1', credentials=credentials)


def carregar_template(nome_usuario, nova_senha):
    """
    Lê o arquivo de template HTML e substitui os placeholders.

    Args:
        nome_usuario (str): nome do destinatário.
        nova_senha (str): senha a ser inserida no template.

    Returns:
        str: HTML com valores preenchidos.
    """
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
        template = file.read()
        return template.replace("{{0}}", nome_usuario).replace("{{1}}", nova_senha)


def criar_email(email_usuario, nome_usuario, nova_senha):
    """
    Monta a mensagem MIME multipart com o template carregado e retorna
    o objeto compatível com a API Gmail (raw base64-url-safe).

    Args:
        email_usuario (str)
        nome_usuario (str)
        nova_senha (str)

    Returns:
        dict: payload {'raw': ...} pronto para envio via service.users().messages().send(...)
    """
    email = MIMEMultipart()
    email['to'] = email_usuario
    email['from'] = formataddr(("Suporte Orac Medicina", EMAIL_USER))
    email['subject'] = "Sua nova senha do Orac Med ⚕️"
    email.attach(MIMEText(carregar_template(
        nome_usuario=nome_usuario, nova_senha=nova_senha), 'html'))

    raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def enviar(email_usuario, nome_usuario, nova_senha):
    """
    Envia o email montado pela função criar_email usando a API Gmail.

    Args:
        email_usuario (str)
        nome_usuario (str)
        nova_senha (str)

    Returns:
        str: email do destinatário (usado como confirmação).
    """
    email = criar_email(email_usuario, nome_usuario, nova_senha)
    service.users().messages().send(
        userId='me',
        body=email
    ).execute()

    return email_usuario
