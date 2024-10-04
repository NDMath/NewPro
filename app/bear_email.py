import email
import imaplib

import json



class EmailClient:
    def __init__(
        self, sender_email: str, sender_password: str, smtp_server: str
    ) -> None:
        """
        Initializes the EmailClient with the sender email, password, and SMTP server.

        Args:
        ----
        sender_email (str): The sender's email address.
        sender_password (str): The sender's password.
        smtp_server (str): The SMTP server to connect to.
        """

        class EmailClient:
            def __init__(self, sender_email, smtp_server):
                self.sender_email = sender_email
                self.smtp_server = smtp_server
                self.sender_password = self._get_password()

        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
    def get_emails(self, mailbox: str = "inbox") -> list:
        """
        Retrieves emails from the specified mailbox.

        Args:
        ----
        mailbox (str, optional): The mailbox to retrieve emails from. Defaults to 'inbox'.

        Returns:
        -------
        list: A list of email messages.
        """
        if not self.sender_email or not self.sender_password or not self.smtp_server:
            raise ValueError("Missing required credentials")

        with imaplib.IMAP4_SSL(self.smtp_server) as connection:
            try:
                connection.login(self.sender_email, self.sender_password)
                connection.select(mailbox, readonly=True)

                status, messages = connection.search(None, "ALL")
                messages = messages[0].split()

                emails = []
                for message_id in messages:
                    status, message_data = connection.fetch(
                        message_id, "(RFC822.HEADER)"
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
sender_email = config['email_client']['sender_email']
smtp_server = config['email_client']['smtp_server']
sender_password = config['email_client']['sender_password']

# Create an instance of the EmailClient
email_client = EmailClient(sender_email, sender_password, smtp_server)

# Get emails
emails = email_client.get_emails()
for email_message in emails:
    print(email_message["Subject"])
    print(email_message["From"])
    print(email_message["To"])
    print(email_message.get_payload())
