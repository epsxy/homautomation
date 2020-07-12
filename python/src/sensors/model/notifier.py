import smtplib
import ssl


class Notifier:
    ctx = None
    mail_srv = 'smtp.gmail.com'
    mail = None
    pwd = None
    port = None
    quota = 10

    def __init__(self, mail: str, pwd: str, port: int):
        self.ctx = ssl.create_default_context()
        self.mail = mail
        self.pwd = pwd
        self.port = port

    def send_mail(self, subject: str, content: str):
        message = 'Subject: {}\n\n{}'.format(subject, content)
        with smtplib.SMTP_SSL(
                self.mail_srv,
                self.port,
                context=self.ctx) as srv:
            if(self.quota > 0):
                self.quota = self.quota - 1
                print('new quota is {}'.format(self.quota))
                srv.login(self.mail, self.pwd)
                srv.sendmail(self.mail, self.mail, message)
            else:
                print('quota exceeded, email not sent')
