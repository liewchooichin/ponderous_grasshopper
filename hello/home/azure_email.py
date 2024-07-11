# Email service from Azure
# Reference: Connect an email domain to a Communication Service Resource
# https://learn.microsoft.com/en-us/azure/communication-services/quickstarts/email/connect-email-communication-resource?pivots=programming-language-python
# az cli to get the key and connection string
# az communication list-key --resource-group DefaultResourceGroup-SEA --name commlcc2002


from azure.mgmt.communication import CommunicationServiceManagementClient #, EmailClient
from azure.identity import DefaultAzureCredential
from decouple import config
import os
from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential

# global variables
#global client
#global email_client

# Credential
def azure_authentication():
    credential = DefaultAzureCredential()
    subscription_id =config("AZURE_SUBSCRIPTION_ID", "")
    global client
    client = CommunicationServiceManagementClient(credential, subscription_id)

    # Authenticate to Communication Service
    key = AzureKeyCredential(config("AZURE_COMM_KEY", ""))
    endpoint = config("AZURE_COMM_ENDPOINT", "")
    global email_client
    email_client = EmailClient(endpoint, key)

# Connect to the email domain
def connect_domain_to_send_email():
    response = client.communication_services.begin_create_or_update(
        resource_group_name=config("AZURE_RESOURCE_GROUP", ""),
        communication_service_name=config("AZURE_EMAIL_DOMAIN_NAME", ""),
        parameters={
            "location": "Global",
            "properties": {
                "dataLocation": config("EMAIL_DATA_LOCATION", ""),
                "linkedDomains": [
                    config("EMAIL_LINKED_DOMAIN_ID", "")
                ],
            }
        },
    ).result()

# Disconnect an email domain from the Communication Service Resource
def disconnect_email_domain():
    response = client.communication_services.begin_create_or_update(
        resource_group_name="<resource-group-name>",
        communication_service_name="<azure-communication-services-resource-name>",
        parameters={
            "location": "Global",
            "properties": {
                "dataLocation": config("EMAIL_DATA_LOCATION", "")
            }
        },
    ).result()


# Try to send email
def send_email(to_email):
    """Send email"""
    try:
        message = {
        "content": {
            "subject": "This is the subject",
            "plainText": "This is the body",
            "html": "<html><h1>This is the body</h1></html>"
        },
        "recipients": {
            "to": [
                {
                    "address": to_email,
                    "displayName": "My Name"
                }
            ]
        },
        "senderAddress":   
            "<donotreply@f0cf672a-d027-4901-bfea-018e517e7e1c.azurecomm.net>"
        }

        poller = email_client.begin_send(message)
        check_status(poller)
        print("Result: " + poller.result())
    except Exception as ex:
        print('Exception:')
        print(ex)

POLLER_WAIT_TIME = 10

def check_status(poller):
    time_elapsed = 0
    while not poller.done():
        print("Email send poller status: " + poller.status())

        poller.wait(POLLER_WAIT_TIME)
        time_elapsed += POLLER_WAIT_TIME

        if time_elapsed > 18 * POLLER_WAIT_TIME:
            raise RuntimeError("Polling timed out.")

    if poller.result()["status"] == "Succeeded":
        print(f"Successfully sent the email (operation id: {poller.result()['id']})")
    else:
        raise RuntimeError(str(poller.result()["error"]))    


def send_with_azure_email(to_email):
    """Main function to send email"""
    azure_authentication()
    connect_domain_to_send_email()
    send_email(to_email)
    disconnect_email_domain()

# Main
if __name__ == "__main__":
    main()