import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Define the path to the credentials JSON file downloaded from Google Developers Console
CREDENTIALS_FILE = r"C:\Users\HP\Desktop\Projects\credentials.json"

# Define the path to the file you want to back up
FILE_TO_BACKUP = r"C:\Users\HP\Documents\Personal Documents\Stock Market.txt"

# Define the destination folder in Google Drive
DESTINATION_FOLDER_ID = '1OjYB51eyhxDkhDLXHJEx-auP16whcNlO'

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)  # This opens a browser for authorization
    return credentials

def upload_file(service, file_path, folder_id):
    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path)
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("File uploaded successfully to Google Drive!")
    except HttpError as error:
        print(f"An error occurred: {error}")
        if error.resp.status == 404:
            print("The specified folder ID was not found. Please check the folder ID.")

def main():
    credentials = authenticate()
    service = build('drive', 'v3', credentials=credentials)
    upload_file(service, FILE_TO_BACKUP, DESTINATION_FOLDER_ID)

if __name__ == '__main__':
    main()
