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


def class_main():
    msg_client = MessageClient()

    # loc = [
    #     {"city": "class 12", "time": "23 min", "distance": "11.56 miles"},
    #     {"city": "class 22", "time": "20 min", "distance": "14.55 miles"},
    #     {"city": "class 32", "time": "25 min", "distance": "17.39 miles"}
    # ]
    loc = [
        {"city": "new line", "time": "23 min", "distance": "11.56 miles"}
    ]


    for item in loc:
        # print(item["city"] + "\n" + item["time"] + "\n" + item["distance"] + "\n")
        msg = item["city"] + "\n" + item["time"] + "\n" + item["distance"] + "\n"
        notification = msg_client.send_notification(msg)
        print(notification.sid)

if __name__ == '__main__':
    pass
    #class_main()
    #main()
    #test()