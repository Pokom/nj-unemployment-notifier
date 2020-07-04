from dotenv import load_dotenv
load_dotenv()

import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_TO_NUMBER = os.getenv('TWILIO_TO_NUMBER')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')