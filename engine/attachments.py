from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build


def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    return credentials


def create_service():
    credentials = authenticate()
    service = build('drive', 'v3', credentials=credentials)
    return service


def create_document(title, file, mimetype):
    service = create_service()
    file_metadata = {'name': str(title)}
    media = MediaFileUpload(file,
                            mimetype=mimetype) # todo: video, gif

    file = service.files().create(body=file_metadata, media_body=media,
                                  fields='id').execute()
    return file.get('id')


def grant_permission(document_id):
    service = build("drive", "v3", credentials=authenticate())
    permission2 = {
        "role": "reader",
        "type": "anyone"
    }
    service.permissions().create(fileId=document_id, body=permission2).execute()


def main(title, file, mimetype):
    file_id = create_document(title, file, mimetype)
    grant_permission(file_id)
    return str(file_id)
