from twilio.rest import Client
import os
from dotenv import load_dotenv
import json

load_dotenv()


class MessageClient:
    def __init__(self):
        print('Initializing messaging client')
        self.ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
        self.AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)
        print('Twilio client initialized')

    @staticmethod
    def get_binding(phone_numbers):
        binding = []
        for num in phone_numbers:
            binding.append(f'{{"binding_type":"sms", "address":"+{num}"}}')
        return binding

    def send_notification(self, msg):
        binding = self.get_binding(json.loads(os.environ.get("PHONE_NUMBERS")))

        notification = self.twilio_client.notify.services(os.environ.get("TWILIO_SERVICE_SID")) \
            .notifications.create(
            to_binding=binding,
            body=msg.replace(r"\n", "\n")
        )
        return notification
