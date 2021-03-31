# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import csv
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main(args):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    with open(args.out, 'w') as f:
        out = csv.DictWriter(f, ["From", "Subject"])
        out.writeheader()
        results = service.users().messages().list(
            userId='me', q=args.q).execute()
        print("Approximately %s results" %
              results.get('resultSizeEstimate', 0))
        total = 0
        while results.get('messages', []):
            for raw_msg in results['messages']:
                msg = service.users().messages().get(
                    userId='me', id=raw_msg['id'], format='metadata').execute()
                headers = msg['payload']['headers']
                from_addr = next(
                    map(lambda d: d['value'], filter(lambda h: h['name'] == 'From', headers)))
                subject = next(
                    map(lambda d: d['value'], filter(lambda h: h['name'] == 'Subject', headers)))
                out.writerow({'From': from_addr, 'Subject': subject})
                total += 1
            print("Wrote", total, "emails")

            if 'nextPageToken' in results:
                results = service.users().messages().list(
                    userId='me', pageToken=results['nextPageToken']).execute()
            else:
                break
        print("Finished, wrote", total, "emails")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q", help="Search query using Gmail search syntax.", required=False)
    parser.add_argument("--label", required=False)
    parser.add_argument("--out", required=False, default="emails.csv")

    main(parser.parse_args())
# [END gmail_quickstart]
