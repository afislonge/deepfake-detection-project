import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def list_files(drive_service, folder_id, mime_type, batch_size=1000):
    """
    Retrieve a list of files or folders from the specified folder ID.

    Args:
    - drive_service: Google Drive service object.
    - folder_id: ID of the folder to list files or folders from.
    - mime_type: MIME type filter for the files to list.
    - batch_size: Number of files to retrieve per API call.

    Returns:
    - List of files or folders.
    """
    page_token = None
    items = []
    while True:
        response = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType = '{mime_type}'",
                                              fields="nextPageToken, files(id, name)",
                                              pageSize=batch_size,
                                              pageToken=page_token).execute()
        items.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return items

def move_real_images(service_account_file, parent_folder_id, destination_folder_id, start_index=0, end_index=None, batch_size=1000):
    """
    Move real images from a parent folder to a destination folder.

    Args:
    - service_account_file: Path to the service account JSON file.
    - parent_folder_id: ID of the parent folder containing the real images.
    - destination_folder_id: ID of the destination folder where real images will be moved.
    - start_index: Starting index of folders to process.
    - end_index: Ending index of folders to process.
    - batch_size: Number of files to process per API call.
    """
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    drive_service = build('drive', 'v3', credentials=credentials)

    results = drive_service.files().list(q=f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
                                          fields="files(id, name)").execute()
    folders = results.get('files', [])

    if end_index is None:
        end_index = len(folders)
    folders = folders[start_index:end_index]

    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['name']
        
        print(f"Accessing folder '{folder_name}'")
        
        files = list_files(drive_service, folder_id, 'image/jpeg', batch_size)
        
        for file in files:
            file_id = file['id']
            file_name = file['name']
            
            copied_file = drive_service.files().copy(fileId=file_id,
                                                     body={'parents': [destination_folder_id],
                                                           'name': file_name}).execute()
        print(f"Done with: '{folder_name}'")
    
    print("All files copied successfully.")

def move_fake_images(service_account_file, source_folder_id, destination_folder_id):
    """
    Move fake images from a source folder to a destination folder.

    Args:
    - service_account_file: Path to the service account JSON file.
    - source_folder_id: ID of the source folder containing the fake images.
    - destination_folder_id: ID of the destination folder where fake images will be moved.
    """
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    drive_service = build('drive', 'v3', credentials=credentials)

    items = list_files(drive_service, source_folder_id, 'image/jpeg')

    num_files_uploaded = 0
    for item in items:
        file_id = item['id']
        file_name = item['name']
        
        copied_file = drive_service.files().copy(fileId=file_id,
                                                 body={'parents': [destination_folder_id],
                                                       'name': file_name}).execute()
        num_files_uploaded += 1
        print(f"Moved file: {file_name}")

    print(f"Total number of JPG files uploaded: {num_files_uploaded}")

# Example usage
if __name__ == "__main__":
    service_account_file = 'service_account.json'
    parent_folder_id = '1tZUcXDBeOibC6jcMCtgRRz67pzrAHeHL'
    destination_folder_id = '15jcev9vedC-0RISrdij2YQJXaAXDFiOl'
    move_real_images(service_account_file, parent_folder_id, destination_folder_id, start_index=8, end_index=10)

    source_folder_id = '18wSFBzxja1axA4NC0XYM1j9sjTBnuM3g'
    destination_folder_id = '19StEBq_VOH-65N18FZu5BjzAquOklzL7'
    move_fake_images(service_account_file, source_folder_id, destination_folder_id)

