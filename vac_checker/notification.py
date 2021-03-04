import secret as s
from twilio.rest import Client


class MessageClient:
    def __init__(self):
        print('Initializing messaging client')
        self.ACCOUNT_SID = s.TWILIO_ACCOUNT_SID
        self.AUTH_TOKEN = s.TWILIO_AUTH_TOKEN
        self.twilio_client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)
        print('Twilio client initialized')

    @staticmethod
    def get_binding(phone_numbers):
        binding = []
        for num in phone_numbers:
            binding.append(f'{{"binding_type":"sms", "address":"+{num}"}}')
        return binding

    def send_notification(self, msg):
        binding = self.get_binding(s.phone_numbers)

        notification = self.twilio_client.notify.services(s.TWILIO_SERVICE_SID) \
            .notifications.create(
            to_binding=binding,
            body=msg.replace(r"\n", "\n")
        )
        return notification
