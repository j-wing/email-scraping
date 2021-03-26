# Setup

1. Clone the repo and `pip install -r requirements.txt`.
1. Sign into the Google account you want to download emails from, then click the "Enable the Gmail API" button here: https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the
1. Download the "credentials.json" file to the repo directory.
1. `python scrape.py -q "<search query> [--out filename.csv]"`
  1. On the first run, it's going to open a Chrome tab for auth. Grant access to the account you want to access
