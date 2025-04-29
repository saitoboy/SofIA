from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Caminho para o JSON da chave de serviço
SERVICE_ACCOUNT_FILE = 'app/utils/credenciais_google.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def extract_folder_id(folder_link):
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', folder_link)
    if match:
        return match.group(1)
    raise ValueError("Não foi possível extrair o ID da pasta do Drive.")

def read_drive_folder(link):
    folder_id = extract_folder_id(link)

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=creds)

    # Lista os arquivos da pasta
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])
    if not items:
        return "A pasta está vazia."

    contents = []

    for file in items:
        file_id = file['id']
        mime_type = file['mimeType']
        name = file['name']

        try:
            if mime_type == 'application/vnd.google-apps.document':
                exported = service.files().export(fileId=file_id, mimeType='text/plain').execute()
                contents.append(exported.decode('utf-8'))

            elif mime_type == 'text/plain':
                from io import BytesIO
                from googleapiclient.http import MediaIoBaseDownload

                request = service.files().get_media(fileId=file_id)
                fh = BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                fh.seek(0)
                contents.append(fh.read().decode('utf-8'))

        except Exception as e:
            print(f"⚠️ Erro ao ler {name}: {e}")

    return "\n\n".join(contents) if contents else "Nenhum conteúdo suportado foi encontrado na pasta."
