import os
from twilio.rest import Client

class SeRe:
    def __init__(self):
        self.sid = "AC5bafbd0fe8e2b75ef39cb4b406298aad"
        self.token = "831a3d688a5e2c0e3c5fc34f60312022"
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
    inter.send_message("message content", '+12265678330')