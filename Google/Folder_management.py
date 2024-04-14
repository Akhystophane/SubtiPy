import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Chargement des credentials à partir du fichier token.json
creds = Credentials.from_authorized_user_file("/Users/emmanuellandau/PycharmProjects/SubtiPy/Google/token.json")
# Supposons que vous avez déjà vos `creds` (objets Credentials) configurés correctement
service = build('drive', 'v3', credentials=creds)

def find_folder_id(folder_name, parent_id=None):
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if files:
        return files[0].get('id')  # Retourne l'ID du premier dossier trouvé
    else:
        return None


def create_folder_path(folder_path):
    folders = folder_path.strip("/").split("/")
    parent_id = None
    for folder in folders:
        folder_id = find_folder_id(folder, parent_id)
        if not folder_id:  # Si le dossier n'existe pas, créez-le
            folder_id = create_drive_folder(folder, parent_id)
        parent_id = folder_id
    return parent_id

def create_drive_folder(name, parent_id=None):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def upload_file_to_folder(filename, filepath, mimetype, parent_id):
    file_metadata = {
        'name': filename,
        'parents': [parent_id]
    }
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')



def upload_folder(local_folder_path, drive_folder_path):
    drive_folder_id = create_folder_path(drive_folder_path)
    for root, dirs, files in os.walk(local_folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            mimetype = 'application/octet-stream'  # ou déterminez le type MIME spécifique si nécessaire
            upload_file_to_folder(filename, filepath, mimetype, drive_folder_id)
            print(f'Uploaded {filename} to Google Drive folder: {drive_folder_path}')


def list_subfolders_in_local_todo(local_todo_path):
    subfolders = []
    for item in os.listdir(local_todo_path):
        if os.path.isdir(os.path.join(local_todo_path, item)):
            subfolders.append(item)
    return subfolders

def list_subfolders_in_local_todo(local_todo_path):
    subfolders = []
    for item in os.listdir(local_todo_path):
        if os.path.isdir(os.path.join(local_todo_path, item)):
            subfolders.append(item)
    return subfolders

def find_folder_id_in_parent(folder_name, parent_id):
    folder_name_escaped = folder_name.replace("'", "''")  # Échappe les apostrophes en les doublant
    query = f"name = '{folder_name_escaped}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents"

    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])
    if not files:
        return None
    return files[0]['id']  # Retourne l'ID du premier dossier correspondant trouvé

from googleapiclient.http import MediaIoBaseDownload
import io

def download_mp4_files_from_drive(drive_folder_id, local_a_roll_path):
    query = f"'{drive_folder_id}' in parents and mimeType='video/mp4'"
    print(query)
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])

    for file in files:
        request = service.files().get_media(fileId=file.get('id'))
        file_path = os.path.join(local_a_roll_path, file.get('name'))
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        print(f"Downloaded {file.get('name')} to {local_a_roll_path}")

def synchronize_subfolders(local_todo_path, drive_todo_id):
    local_subfolders = list_subfolders_in_local_todo(local_todo_path)
    for local_subfolder in local_subfolders:
        drive_subfolder_id = find_folder_id_in_parent(local_subfolder, drive_todo_id)
        if drive_subfolder_id:
            local_a_roll_path = os.path.join(local_todo_path, local_subfolder, "a-roll")
            if not os.path.exists(local_a_roll_path):
                os.makedirs(local_a_roll_path)
            download_mp4_files_from_drive(drive_subfolder_id, local_a_roll_path)

# upload_folder("/Users/emmanuellandau/Documents/EditLab/READY/1560", "TODO/1560")
#
# synchronize_subfolders("/Users/emmanuellandau/Documents/EditLab/READY", find_folder_id("TODO"))