# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import random as rnd
import time

import luigi


class Configuration(luigi.Task):
    seed = luigi.IntParameter()

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget('/tmp/Config_%d.txt' % self.seed)

    def run(self):
        time.sleep(5)
        rnd.seed(self.seed)

        result = ','.join(
            [str(x) for x in rnd.sample(list(range(300)), rnd.randint(7, 25))])
        with self.output().open('w') as f:
            f.write(result)


class Data(luigi.Task):
    magic_number = luigi.IntParameter()

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget('/tmp/Data_%d.txt' % self.magic_number)

    def run(self):
        time.sleep(1)
        with self.output().open('w') as f:
            f.write('%s' % self.magic_number)


class Dynamic(luigi.Task):
    seed = luigi.IntParameter(default=1)

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.

        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget('/tmp/Dynamic_%d.txt' % self.seed)

    def run(self):
        # This could be done using regular requires method
        config = self.clone(Configuration)
        yield config

        with config.output().open() as f:
            data = [int(x) for x in f.read().split(',')]

        # ... but not this
        data_dependent_deps = [Data(magic_number=x) for x in data]
        yield data_dependent_deps

        with self.output().open('w') as f:
            f.write('Tada!')

        # and in case data is rather long, consider wrapping the requirements
        # in DynamicRequirements and optionally define a custom complete method
        def custom_complete(complete_fn):
            # example: Data() stores all outputs in the same directory, so avoid doing len(data) fs
            # calls but rather check only the first, and compare basenames for the rest
            # (complete_fn defaults to "lambda task: task.complete()" but can also include caching)
            if not complete_fn(data_dependent_deps[0]):
                return False
            paths = [task.output().path for task in data_dependent_deps]
            basenames = os.listdir(os.path.dirname(paths[0]))  # a single fs call
            return all(os.path.basename(path) in basenames for path in paths)

        yield luigi.DynamicRequirements(data_dependent_deps, custom_complete)


if __name__ == '__main__':
    luigi.run()