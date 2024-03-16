import luigi
from tasks import *
from tasks.task import Task

class Main(Task):
    def run(self):

        info = Info()
        yield info
        content = info.output()

        email = EmailSend(subject='Relay Mail', message=content, sendTo='hello@hotmail.com')
        yield email


if __name__ == '__main__':
    luigi.build(
        [Main()],
        local_scheduler=False,
    )

