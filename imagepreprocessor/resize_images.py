import io
import shutil
import os.path
import tempfile
from PIL import Image
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def initialize_drive_service():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    return service

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


# Google Drive file list
def list_drive_files(service, folder_id):
    files = []
    page_token = None

    while True:
        response = service.files().list(q=f"'{folder_id}' in parents",
                                         fields="nextPageToken, files(id, name)",
                                         pageToken=page_token).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break

    return files

# Google Drive download file
def download_drive_file(service, file_id, file_name):
    file = service.files().get(fileId=file_id).execute()
    if 'mimeType' in file and 'application/vnd.google-apps' in file['mimeType']:
        request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
    else:
        request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# Image Resize and save it in a stream
def resize_image(image_stream, new_size=(256, 256)):
    img = Image.open(image_stream)
    img_resized = img.resize(new_size, Image.LANCZOS)
    img_resized_stream = io.BytesIO()
    img_resized.save(img_resized_stream, format='JPEG')
    img_resized_stream.seek(0)
    return img_resized_stream


# Función para subir un archivo a Google Drive
def upload_drive_file(service, file_stream, folder_id, file_name):
    # Convert BytesIO object to bytes
    file_bytes = file_stream.getvalue()

    # Upload the file content to Google Drive
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaIoBaseUpload(file_stream, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file.get('id')

# Image processing
def process_images():
    service = initialize_drive_service()

    folder_id = '15jcev9vedC-0RISrdij2YQJXaAXDFiOl' #Project Real source
    # folder_id = '19StEBq_VOH-65N18FZu5BjzAquOklzL7' #Project Fake source
    # folder_id = '1bWf83LgiUK1Z8dU-R3d1Pvd8N_DhScuv' # Test

    resized_folder_id = '1zuxCn44gEi7t6trQsdW64wJu-S96eTMj' #Project Real target
    # resized_folder_id = '1UlvNsoDKKLb88Q9_i3MAkefVILA7or2R' #Project Fake target
    # resized_folder_id = '1HpfeqlsUp9OZ91EbyMwChEcz8L1PA3mP' # Test

    files = list_drive_files(service, folder_id)

    for file in files:
        file_stream = download_drive_file(service, file['id'], file['name'])

        # Convert BytesIO to bytes
        file_bytes = file_stream.read()

        resized_image_stream = resize_image(io.BytesIO(file_bytes))

        gdrive_file = upload_drive_file(service, resized_image_stream, resized_folder_id, f"Resized_{file['name']}")

        print(f"Gdrive File created: {gdrive_file} - {datetime.now()}")
        '''
        print(f"{file['id']} - {file['name']}")
        '''

    #print("Images were resized and uploaded to Google Drive.")

# Call main function
process_images()