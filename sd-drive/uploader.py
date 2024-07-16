import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def authenticate_google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(service, file_path, file_name, folder_id=None):
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File ID: {file.get('id')}")


def push_push(file_path, file_name):
    service = authenticate_google_drive()
    upload_to_drive(service, file_path, file_name)

def up_up(inputs):
    input_lines = [line.strip() for line in inputs.strip().splitlines()]

    if not inputs.strip():
        yield "Missing: [ Input ]", True
        return

    task_task = []

    for line in input_lines:
        parts = line.split()
        input_path = parts[0]
        input_path = input_path.strip('"').strip("'")

        given_fn = None
        ex_ext = None

        if '-' in parts:
            given_fn_fn = parts.index('-') + 1
            if given_fn_fn < len(parts):
                given_fn = parts[given_fn_fn]
            else:
                yield "Invalid usage\n[ - ]", True
                return

        if '--' in parts:
            ex_ext_ext = parts.index('--') + 1
            if ex_ext_ext < len(parts):
                ex_ext = parts[ex_ext_ext:]
            else:
                yield "Invalid usage\n[ -- ]", True
                return

        full_path = Path(input_path) if not input_path.startswith('$') else None

        if full_path:
            if full_path.is_file():
                type_ = "file"
            elif full_path.is_dir():
                type_ = "folder"
            else:
                type_ = "unknown"
        else:
            yield f"{input_path}\nInput Path does not exist.", True
            return

        if given_fn and not Path(given_fn).suffix and full_path.is_file():
            given_fn += full_path.suffix

        task_task.append((full_path, given_fn or full_path.name, type_))

    for file_path, file_name, type_ in task_task:
        yield f"Uploading: {file_name}", False

        try:
            push_push(file_path=str(file_path), file_name=file_name)
            yield f"Uploaded: {file_name}", False
        except Exception as e:
            yield f"Error uploading {file_name}: {str(e)}", True

def uploader(inputs, box_state=[]):
    output_box = box_state if box_state else []

    for _text, _flag in up_up(inputs):
        if not _flag:
            if "Uploading" in _text:
                yield _text, "\n".join(output_box)
            yield _text, "\n".join(output_box)
        else:
            output_box.append(_text)
            
    catcher = ["not", "Missing", "Error", "Invalid"]
    
    if any(asu in wc for asu in catcher for wc in output_box):
        yield "Error", "\n".join(output_box)
    else:
        yield "Done", "\n".join(output_box)
        
    return output_box
