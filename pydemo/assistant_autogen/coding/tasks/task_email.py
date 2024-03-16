import luigi
from tasks.task import Task 

def dummy_job(obj:Task, t=0.1):
        import time
        # set status messages during the workload
        for i in range(101):
            # do some hard work here
            time.sleep(t)
            obj.set_status_message("Progress: %d / 100" % i)
            # displays a progress bar in the scheduler UI
            obj.set_progress_percentage(i)


class EmailSend(Task):
    # x = luigi.IntParameter()
    # y = luigi.IntParameter(default=45)
    message = luigi.Parameter(default='')
    sendTo = luigi.Parameter(default='')
    subject = luigi.Parameter(default='')

    def run(self):
        dummy_job(self)
        pass


if __name__ == '__main__':
    luigi.run()