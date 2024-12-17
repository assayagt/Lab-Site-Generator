import os
import json
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the required Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class EmailNotification:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send_email(self):
        """Authenticate and send the email."""
        service = self.authenticate_gmail_api_env()

        try:
            message = self.create_message()
            send_message = service.users().messages().send(userId="me", body=message).execute()
            print(f'Message sent! Message ID: {send_message["id"]}')
            return send_message
        except HttpError as e:
            raise Exception("An error occurred while sending the email.") from e

    def create_message(self):
        """Create an email message in the required format."""
        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {self.recipient}\r\nSubject: {self.subject}\r\n\r\n{self.body}".encode('UTF-8')
            ).decode('utf-8')
        }
        return message

    def authenticate_gmail_api_env(self):
        """Authenticate to the Gmail API."""
        creds = None

        # Check for existing credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # Refresh or create credentials if none exist
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_json = os.getenv('GOOGLE_CREDENTIALS')
                if not credentials_json:
                    raise Exception("GOOGLE_CREDENTIALS environment variable is not set.")

                with open(credentials_json, "r") as file:
                    credentials_dict = json.load(file)

                # Use a temporary file to comply with API requirements
                with open("temp_credentials.json", "w") as temp_file:
                    json.dump(credentials_dict, temp_file)

                flow = InstalledAppFlow.from_client_secrets_file(
                    "temp_credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

                # Cleanup the temporary file
                os.remove("temp_credentials.json")

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)
