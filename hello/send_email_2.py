# Using connection string to connect to EmailClient

from azure.communication.email import EmailClient
from decouple import config
def main():
    try:
        connection_string = config("EMAIL_CONNECTION_STRING", "")
        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@f0cf672a-d027-4901-bfea-018e517e7e1c.azurecomm.net",
            "recipients":  {
                "to": [{"address": "<MY_EMAIL_ADDRESS>" }],
            },
            "content": {
                "subject": "Test Email 2",
                "plainText": "Hello world 2 via email.",
            }
        }

        poller = client.begin_send(message)
        result = poller.result()

    except Exception as ex:
        print(ex)
main()
