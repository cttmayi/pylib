
# my_module.py, available in your sys.path
import luigi

class MyTask(luigi.Task):
    x = luigi.IntParameter()
    y = luigi.IntParameter(default=45)

    def run(self):
        import time

        self.set_tracking_url("http://...")

        # set status messages during the workload
        for i in range(100):
            # do some hard work here
            time.sleep(1)
            self.set_status_message("Progress: %d / 100" % i)
            # displays a progress bar in the scheduler UI
            self.set_progress_percentage(i)


        print(self.x + self.y)

if __name__ == '__main__':
    luigi.run()