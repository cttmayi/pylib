import luigi


class Task(luigi.Task):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_complete = False

    def on_success(self):
         self.is_complete = True

    def complete(self):
        return self.is_complete