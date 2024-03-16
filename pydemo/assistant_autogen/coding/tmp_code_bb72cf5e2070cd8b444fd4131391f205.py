import luigi
from tasks.task_email import EmailSend

email = EmailSend(subject='Autogen框架评价', message='Autogen是一个好框架', sendTo='Ling@example.com')

if __name__ == '__main__':
    luigi.build([email])