import base64
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.errors import HttpError
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class EmailNotification:

    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send_email(self):
        # Authenticate with Gmail API
        service = self.authenticate_gmail_api()

        # send the mail
        try:
            message = self.create_message()
            send_message = service.users().messages().send(userId="me", body=message).execute()
            print(f'Message Id: {send_message["id"]}')
            return send_message
        except HttpError as e:
            raise Exception(ExceptionsEnum.ERROR_SENDING_EMAIL)

    # Create the message
    def create_message(self):
        message = {
            'raw': base64.urlsafe_b64encode(f"To: {self.recipient}\r\nSubject: {self.subject}\r\n\r\n{self.body}".encode('UTF-8')).decode(
                'utf-8')
        }
        return message

    # Authenticate and get the service
    def authenticate_gmail_api(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                credentials_path = os.path.join(base_dir, "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

