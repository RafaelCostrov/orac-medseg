"""
Módulo services.google_services.google_service

Fornece utilitário para autenticação com a API do Google Drive usando
uma conta de serviço e delegação para um usuário (SERVICE_ACCOUNT_FILE,
EMAIL_USER e SCOPES devem estar definidos no .env).

Funções:
- acessando_drive(): retorna uma instância do serviço Drive v3 autenticada.
"""
import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()


def acessando_drive():
    """
    Cria e retorna o objeto de serviço do Google Drive (v3).

    Lê SERVICE_ACCOUNT_FILE, EMAIL_USER e SCOPES do ambiente, carrega as
    credenciais da conta de serviço e delega para EMAIL_USER.

    Returns:
        googleapiclient.discovery.Resource: cliente para interagir com o Drive.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(
        BASE_DIR, os.getenv('SERVICE_ACCOUNT_FILE'))
    EMAIL_USER = os.getenv('EMAIL_USER')
    SCOPES = os.getenv('SCOPES_DRIVE').split(',')
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES).with_subject(EMAIL_USER)
    drive_service = build("drive", "v3", credentials=creds)
    return drive_service
