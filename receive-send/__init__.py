import os
from twilio.rest import Client

class SeRe:
    def __init__(self):
        values = open("secrets.hidden", "r").read().split()
        self.sid = values[0]
        self.token = values[1]
        self.client = Client(self.sid, self.token)
        self.default_number = "+12262708145"

    def send_message(self, body, number_to, number_from = None):
        if number_from is None:
            number_from = self.default_number
        message = self.client.messages \
            .create(
            body=body,
            from_=number_from,
            to=number_to
        )



if __name__ == "__main__":
    inter = SeRe()
    inter.send_message("message content", '+15191234123')
