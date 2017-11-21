import luigi
import os
import pandas as pd
import train

# How to deal with multiple input/outputs: https://groups.google.com/forum/#!topic/luigi-user/ybWN_lEcPrU

class Cleanup(luigi.Task):
    """
    This task removes all output files for all tasks effectively marking these as incomplete.
    """
    priority = 100

    def run(self):
        if(os._exists('train.csv')):
            os.remove('train.csv')

    def complete(self):
        return True

class CollectData(luigi.Task):
    """
    This task checks input data files are available.
    """
    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task ensures all input data files exist on the local filesystem.
        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return { 'places': luigi.LocalTarget('data/geoplaces2.csv'),
                 'parking': luigi.LocalTarget('data/chefmozparking.csv'),
                 'rating': luigi.LocalTarget('data/rating_final.csv') }

    def run(self):
        print('Starting to ensure input data')
        raise Exception('Assumption failed: at least one input data file is missing.')

class PrepareData(luigi.Task):
    """
    This task ...
    """

    def requires(self):
        return CollectData()

    def output(self):
        return { 'data': luigi.LocalTarget('train.csv'),
                 'mapping' : luigi.LocalTarget('mapping.dat') }

    def run(self):
        print('Starting to prepare data')
        mt = train.ModelTrainer()
        df = mt.LoadRawData(self.input()['places'].path, self.input()['parking'].path, self.input()['rating'].path)
        mt.TransformData()
        mt.ExportTrainingData(self.output()['data'].path)
        mt.ExportMappingData(self.output()['mapping'].path)



class TrainModel(luigi.Task):

    def requires(self):
        return PrepareData()

    def output(self):
        return { 'model': luigi.LocalTarget('model.dat'),
                 'mapping': luigi.LocalTarget(self.input()['mapping'].path) }

    def run(self):
        print('Starting to train prediction model')
        mt = train.ModelTrainer()
        mt.LoadTrainingData(self.input()['data'].path)
        mt.TrainModel()
        mt.ExportModel(self.output()['model'].path)

class DeployModel(luigi.Task):

    def requires(self):
        return TrainModel()

    def run(self):
        print('Starting to deploy prediction model')


if __name__ == "__main__":
    luigi.run(["--local-scheduler"], main_task_cls = TrainModel)
