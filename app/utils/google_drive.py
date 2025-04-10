from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import os

# Caminho para o arquivo de credenciais JSON
SERVICE_ACCOUNT_FILE = 'path/to/credentials.json'  # Substitua pelo caminho correto
SCOPES = ['https://www.googleapis.com/auth/drive']

def list_files_in_folder(folder_id: str):
    """
    Lista os arquivos em uma pasta específica no Google Drive.
    
    Args:
        folder_id (str): ID da pasta no Google Drive.
    
    Returns:
        list: Lista de arquivos na pasta.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    # Listar arquivos na pasta
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def download_file(file_id: str, file_name: str, save_path: str):
    """
    Faz o download de um arquivo do Google Drive.
    
    Args:
        file_id (str): ID do arquivo no Google Drive.
        file_name (str): Nome do arquivo.
        save_path (str): Caminho para salvar o arquivo localmente.
    """
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(save_path, file_name)
    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
    return file_path