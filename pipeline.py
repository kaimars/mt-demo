import luigi
import os

class Reset(luigi.Task):
    """
    This task removes all output files for all tasks effectively marking these as incomplete.
    """

    def run(self):
        os.remove('train.csv')


class PrepareData(luigi.Task):
    """
    This task ...
    """
    # TODO: split the task to CollectData and MapData ?
    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.
        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("train.csv")

    def run(self):
        print('Starting to prepare data')
        with self.output().open('w') as out_file:
            out_file.write('Done')



class TrainModel(luigi.Task):

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.Streams`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return PrepareData()

    def run(self):
        print('Starting to train prediction model')

class DeployModel(luigi.Task):

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.Streams`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return TrainModel()

    def run(self):
        print('Starting to deploy prediction model')


if __name__ == "__main__":
    luigi.run(["--local-scheduler"], main_task_cls = TrainModel)
    #luigi.run(["--local-scheduler"], main_task_cls=Reset)