import email
import imaplib

import json


class EmailClient:

    def __init__(
        self,
        recipient_email: str,
        recipient_password: str,
        imap_server: str
    ) -> None:

        """
        Initializes the EmailClient with the sender email, password, and SMTP server.

        Args:
        ----
        recipient_email (str): The sender's email address.
        recipient_password (str): The sender's password.
        imap_server (str): The SMTP server to connect to.
        """

        self.recipient_email = recipient_email
        self.recipient_password = recipient_password
        self.imap_server = imap_server

    def get_emails(
        self,
        mailbox: str = "inbox"
    ) -> list:

        """
        Retrieves emails from the specified mailbox. Using IMAP.

        Args:
        ----
        mailbox (str, optional): The mailbox to retrieve emails from. Defaults to 'inbox'.

        Returns:
        -------
        list: A list of email messages.
        """

        if not self.recipient_email or not self.recipient_password or not self.imap_server:
            raise ValueError("Missing required credentials")

        if not isinstance(mailbox, str):
            raise TypeError("mailbox must be a string")

        with imaplib.IMAP4_SSL(self.imap_server) as connection:
            try:
                connection.login(self.recipient_email, self.recipient_password)
                connection.select(mailbox, readonly=True)

                status, messages = connection.search(None, "ALL")
                if status != "OK":
                    raise RuntimeError(f"Unable to search emails: {status}")

                messages = messages[0].split()

                emails = []
                for message_id in messages:
                    status, message_data = connection.fetch(
                        message_id, "(RFC822.HEADER)"
                    )
                    if status != "OK":
                        raise RuntimeError(
                            f"Unable to fetch email {message_id}: {status}"
                        )
                    raw_message = message_data[0][1]
                    email_message = email.message_from_bytes(raw_message)
                    emails.append(email_message)

            except (imaplib.IMAP4.error, ConnectionResetError) as e:
                raise RuntimeError(f"Unable to fetch emails: {e}")

        return emails

# Load config file
with open('config.json', 'r') as f:
    config = json.load(f)

# Access credentials
imap_server = config['email_client']['imap_server']
recipient_email = config['email_client']['recipient_email']
recipient_password = config['email_client']['recipient_password']

# Create an instance of the EmailClient
email_client = EmailClient(recipient_email, recipient_password, imap_server)

# Get emails
emails = email_client.get_emails()
for email_message in emails:
    print(email_message["Subject"])
    print(email_message["From"])
    print(email_message["To"])
    print(email_message.get_payload())
