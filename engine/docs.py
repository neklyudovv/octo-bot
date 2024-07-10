from google.oauth2 import service_account
from googleapiclient.discovery import build


def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    return credentials


def create_service():
    credentials = authenticate()
    service = build('docs', 'v1', credentials=credentials)
    return service


def create_document(title):
    service = create_service()
    document = service.documents().create(body={'title': title}).execute()
    document_id = document['documentId']
    grant_permission(document_id)
    # print(f'Создан новый документ с ID: {document_id}')
    return document_id


def grant_permission(document_id):
    service = build("drive", "v3", credentials=authenticate())
    permission2 = {
        'type': 'anyone',
        'role': 'writer',
    }
    service.permissions().create(fileId=document_id, body=permission2).execute()


def insert_text(document_id, text):
    service = create_service()

    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1
                },
                'text': text
            }
        }
    ]

    service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    print('Текст успешно вставлен в документ')


def main(text):
    document_id = '1l-AeWtEOMdBAwWhX31SjHxPk6gYoZ9h5wBCS6O3FyWw'
    insert_text(document_id, text + '\n\n----------------\n')
