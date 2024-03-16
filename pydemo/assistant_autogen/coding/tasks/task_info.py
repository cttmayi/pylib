import luigi
from tasks.task import Task 




class Info(Task):
    message = luigi.Parameter()

    content = None

    def output(self):
        raise Exception('Not implemented')

        return self.content


    def run(self):
        self.content = 'Hello World'
        pass


if __name__ == '__main__':
    luigi.run()