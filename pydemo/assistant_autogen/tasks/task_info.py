import luigi
from tasks.task import Task



class Info(Task):
    content = ''

    def output(self):
        return self.content


    def run(self):
        self.content = 'Hello World'
        pass


if __name__ == '__main__':
    luigi.run()