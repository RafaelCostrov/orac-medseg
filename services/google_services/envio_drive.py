"""
Módulo services.google_services.envio_drive

Funções utilitárias para upload e remoção de arquivos no Google Drive usando
o serviço retornado por services.google_services.google_service.acessando_drive.

Depende da variável de ambiente PASTA_DRIVE_FOTOS (PASTA_RAIZ_ID).
Funções:
- salvar_drive(nome_arquivo, email_usuario, nome_usuario): faz upload e retorna id do arquivo.
- remover_drive(id_arquivo): remove arquivo pelo id.
"""
import os
from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload
from services.google_services.google_service import acessando_drive


load_dotenv()
PASTA_RAIZ_ID = os.getenv('PASTA_DRIVE_FOTOS')


def salvar_drive(nome_arquivo, email_usuario, nome_usuario):
    """
    Faz upload de um arquivo local para a pasta especificada no Drive.

    Args:
        nome_arquivo (str): caminho local do arquivo a enviar.
        email_usuario (str): usado para compor o nome do arquivo no Drive.
        nome_usuario (str): usado para compor o nome do arquivo no Drive.

    Returns:
        str: id do arquivo criado no Drive.
    """
    drive = acessando_drive()
    pasta_id = PASTA_RAIZ_ID

    nome = f"{email_usuario}_{nome_usuario}"

    file_metadata = {
        'name': nome,
        'parents': [pasta_id]
    }

    media = MediaFileUpload(nome_arquivo, resumable=True)
    arquivo = drive.files().create(body=file_metadata,
                                   media_body=media, fields='id').execute()
    return arquivo.get('id')


def remover_drive(id_arquivo):
    """
    Remove um arquivo do Drive pelo seu id.

    Args:
        id_arquivo (str)

    Returns:
        bool: True se a operação foi executada (lança exceção em caso de erro).
    """
    drive = acessando_drive()
    drive.files().delete(fileId=id_arquivo).execute()
    return True
