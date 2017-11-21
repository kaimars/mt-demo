import luigi
import os
import train
import shutil

# How to deal with multiple input/outputs: https://groups.google.com/forum/#!topic/luigi-user/ybWN_lEcPrU

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
    This task prepares training data. Encoded trainig data is written to train.csv and used mappings
    are dumped to mapping.dat file.
    """

    def requires(self):
        return CollectData()

    def output(self):
        return { 'data': luigi.LocalTarget('train.csv'),
                 'mapping' : luigi.LocalTarget('mapping.dat') }

    def run(self):
        print('Starting to prepare data')
        mt = train.ModelTrainer()
        mt.LoadRawData(self.input()['places'].path, self.input()['parking'].path, self.input()['rating'].path)
        mt.TransformData()
        mt.ExportTrainingData(self.output()['data'].path)
        mt.ExportMappingData(self.output()['mapping'].path)


class TrainModel(luigi.Task):
    """
    This task trains model and writes trained model to file model.dat
    """

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
    """
    This task sends new prediction model and mapping files to web service for consumption.
    """
    #TODO: send also 'reload model' command to web service, currently must restart web server for that

    def requires(self):
        return TrainModel()

    def complete(self):
        return False

    def run(self):
        print('Starting to deploy new prediction model')
        shutil.copyfile(self.input()['model'].path, 'api/model.dat')
        shutil.copyfile(self.input()['mapping'].path, 'api/mapping.dat')


if __name__ == "__main__":
    luigi.run(["--local-scheduler"], main_task_cls = DeployModel)
