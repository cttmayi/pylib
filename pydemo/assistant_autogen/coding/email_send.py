# filename: email_send.py
import luigi
from tasks.task_email import EmailSend

class SendEmailTask(luigi.Task):
    def requires(self):
        return []

    def run(self):
        email = EmailSend(subject='关于你父亲的消息', message='你的父亲现在在中国。', sendTo='ling.yuan@mediatek.com')
        yield email

    def output(self):
        return luigi.LocalTarget('email_sent.txt')

if __name__ == '__main__':
    luigi.build([SendEmailTask()])