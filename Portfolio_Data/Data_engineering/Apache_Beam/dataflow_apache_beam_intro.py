# -*- coding: utf-8 -*-
"""Dataflow_Apache-beam_intro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aLRG4KHyC5OhfEL6UzX9OxC6Ukm4tnss

### On importe les packages apaches beam que l'on souhaite utiliser
"""

import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from sys import argv

"""### On instancie les variables Project ID de notre compte GCP et le schema pour la table de destination BigQuery"""

PROJECT_ID = 'projet-delphine'
SCHEMA = 'annee:STRING,groupe:INTEGER,sexe:STRING,nombre:INTEGER,motif:STRING,type_sanction:STRING,source:STRING,conseil_discpline:STRING'

"""### On parse nos argument avec la méthode parser"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    known_args = parser.parse_known_args(argv)

def del_unwanted_cols(data):
    """Delete the unwanted columns"""
    del data['sexe']
    del data['conseil_discpline']
    return data

# Create and set your PipelineOptions.
# For Cloud execution, specify DataflowRunner and set the Cloud Platform
# project, job name, temporary files location, and region.
# For more information about regions, check:
# https://cloud.google.com/dataflow/docs/concepts/regional-endpoints
options = PipelineOptions(
    flags=argv,
    runner='DataflowRunner',
    project='projet-delphine',
    job_name='pipeline',
    temp_location='gs://projet-delphine/temp',
    region='us-east1-c'
    
    
    ')

# Create the Pipeline with the specified options.
# with beam.Pipeline(options=options) as pipeline:
#   pass  # build your pipeline here.

"""### On met en place notre pipeline"""

# On instancie notre pipeline dans une variable

p1 = beam.Pipeline(options=options)

# On crée notre Pipeline

attendance_count =   (
                          p1
                          | 'Lecture des données' >> beam.io.ReadFromText('gs://df-pipeline-1/sanctionspolice.csv', skip_header_lines =1)
                          | 'Séparation des lignes' >> beam.Map(lambda x: x.split(','))
                          | 'Transformation en format dict' >> beam.Map(lambda x: {"annee": x[0], "groupe": x[1], "sexe": x[2], "nombre": x[3], "motif": x[4], "type_sanction": x[5], "source": x[6], "conseil_discpline": x[7]}) 
                          | 'Supprimer les collones inutiles' >> beam.Map(del_unwanted_cols)
                          | 'Ecriture dans BigQuery' >> beam.io.WriteToBigQuery(
                              '{0}:sanction.sanctionspolice'.format(PROJECT_ID),
                              schema=SCHEMA,
                              write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

"""### On charge notre pipeline

> Bloc en retrait


"""

result = p1.run()
result.wait_until_finish()