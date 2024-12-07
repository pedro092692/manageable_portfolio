import smtplib
from dotenv import load_dotenv
import os


class Contact:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv('USER')
        self.password = os.getenv('PASSWORD')
        self.server = os.getenv('SERVER')
        self.port = 587

    def send_email(self, message: str, email_sender: str, name: str):
        try:
            with smtplib.SMTP(self.server, self.port) as connection:
                connection.starttls()
                connection.login(self.user, self.password)
                connection.sendmail(to_addrs=[self.user], from_addr=self.user,
                                    msg=f'Subject: Message from your Portfolio'
                                    f"\n\n {name} wants to contact to you \n Email: {email_sender} \n {message}")
                return True

        except smtplib.SMTPException as e:
            print(f'There was a problem trying to connect with the email server: {e}')

            return False

