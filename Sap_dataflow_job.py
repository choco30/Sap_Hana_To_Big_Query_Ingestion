#Java dk 8, mssql-jdbc-10.21 is required to setup and need to be paced into a gcs bucket which can be collectively installed as atar file at run time
#Jaydebeapi,pandas,gcsfs,sqlalchemy are the dependencied needs to be installed at run time on the worker nodes>the dependency are defined in aform of setup .py file which is passed on time of running the code
# The code has been successfully tested on apache beam version 2.39(by manually limiting the PROTOBUF dependency to 3.20) and 2.41
import apache_beam as beam

import os
import argparse
import logging
import pandas as  pd
from oauth2client.client import GoogleCredentials
from datetime import datetime,date,timedelta
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions,SetupOptions
from google.cloud import secretmanager
from json import loads
secret_client = secretmanager.SecretManagerServiceClient()
project_id = "project_id"
secret_response = secret_client.access_secret_version(
    {"name": "projects/"+project_id+"/secrets/sap_credentials/versions/latest"})
secret_response = secret_response.payload.data.decode("utf-8")
my_credentials= loads(secret_response)
username_sap=my_credentials["user"]
password_sap=my_credentials["password"]
address_sap=my_credentials["address"]
port_sap=my_credentials["port"]
project_gcp=my_credentials["project_id"]
dataset_gcp=my_credentials["dataset_id"]
class setenv(beam.DoFn): 
      def process(self,context,df_Bucket):
          #import jaydebeapi
          import pandas as pd
          #src1='gs://gcp01-sb-krnospbi-dataflow-bucket/JAVA_JDK_AND_JAR'
          src1='gs://'+df_Bucket+'/JAVA_JDK_AND_JAR'
          os.system('gsutil cp '+src1 + '/jdk-8u202-linux-x64.tar.gz /tmp/')
          logging.info('Jar copied to Instance..')
          logging.info('Java Libraries copied to Instance..')
          os.system('mkdir -p /usr/lib/jvm  && tar zxvf /tmp/jdk-8u202-linux-x64.tar.gz -C /usr/lib/jvm  && update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_202/bin/java" 1 && update-alternatives --config java')
          logging.info('Enviornment Variable set.')
          return list("1")
class readandwrite(beam.DoFn):
    def process(self, context, address_sap,port_sap,username_sap,password_sap,project_id,dataset_id):

        from hdbcli import dbapi
        import pandas as pd
        import json
        import fsspec
        import gcsfs
        from google.cloud import bigquery
        from google.cloud import storage
        client = bigquery.Client()
        conn = dbapi.connect(
            address=address_sap,
            port=port_sap,
            user=username_sap, 
            password=password_sap)
        bigquerySchema=[]
        conn.isconnected()
        cursor = conn.cursor()
        list1=['table1','table2','table3','sandy']
        
        #header={'table1':["id","name"],'table2':["id","name"],
        #'table3':["id","name"],'sandy':["id","age"]}
        for i in list1:
            query="select * from {0}".format(i)
            headers=[]
            schema=i+".json"
            url="gs://schema_bucket/{0}".format(schema)
            #url="gs://"+gcs_name+"/"+".{}".format(schema)
            #url='gs://'+gcs_name+"/"+".{}".format(schema)
            #print(url)
            gcs_file_system = gcsfs.GCSFileSystem(project=project_id)
            gcs_json_path = url
            with gcs_file_system.open(gcs_json_path) as f:
                bigqueryColumns = json.load(f)
            for j in bigqueryColumns:
                headers.append(j['name'])
            cursor.execute(query)
            result = cursor.fetchall()
            #print(header[i])
            df=pd.DataFrame(result,columns=headers)
            #print(df)
            table_id = project_id+"."+dataset_id+".{0}".format(i)

                #print(bigqueryColumns)
                #bigqueryColumns = json.load(f.download_as_text(encoding="utf-8"))
                
            for col in bigqueryColumns:
                bigquerySchema.append(bigquery.SchemaField(col['name'], col['type']))
            job_config = bigquery.LoadJobConfig(    
            schema=bigquerySchema,
            write_disposition="WRITE_TRUNCATE",
        )
            job = client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )  
            job.result()  
            table = client.get_table(table_id)  
            
            bigquerySchema.clear()

def run():    
       
    try: 
        parser = argparse.ArgumentParser()
        
        Stored and Fetched through secret Manager At the start of the code but can also be provide when triggering dataflow job through Airflow
        other pipeline arguments are provided at run time.
        """
        parser.add_argument(
            '--urlendpoint',
            required=True,
            help= ('SAP HANA cloud URL Endpoint')
            )
        parser.add_argument(
            '--Port_no',
            required=True,
            help= ('Port Number of SAP HANA Cloud')
            )
        parser.add_argument(
            '--User_name',
            required=True,
            help= ('User Name of SAP HANA ')
            )
        parser.add_argument(
            '--user_password',
            required=True,
            help= ('Password of SAP HANA User')
            )     
        
        parser.add_argument(
            '--myid',
            required=True,
            help= ('GCP Project ID')
        )
        
        parser.add_argument(
            '--gcp_datasetid',
            required=True,
            help= ('GCP BigQuery Dataset ID')
        )
        """
        parser.add_argument(
            '--dfBucket',
            required=True,
            help= ('Bucket where JARS/JDK is present')
            )
               
        known_args, pipeline_args = parser.parse_known_args()

        global df_Bucket
        df_Bucket = known_args.dfBucket
        """
        global url_endpoint
        url_endpoint = known_args.urlendpoint
        global port
        port = known_args.Port_no
        global user
        user = known_args.User_name
        global password 
        password = known_args.user_password
        global project_id 
        project_id = known_args.myid
        global dataset_id 
        dataset_id = known_args.gcp_datasetid
        """
       
        pipeline_options = PipelineOptions(pipeline_args)
        pcoll = beam.Pipeline(options=pipeline_options)
        #pipeline_options.view_as(SetupOptions).save_main_session = True
        
        logging.info("Pipeline Starts")
        dummy= pcoll | 'Initializing..' >> beam.Create(['1'])
        dummy_env = dummy | 'Setting up Instance..' >> beam.ParDo(setenv(),df_Bucket)
        read_records=(dummy_env | 'Processing' >>  beam.ParDo(readandwrite(),address_sap,port_sap,username_sap,password_sap,project_gcp,dataset_gcp))
        p=pcoll.run()
        logging.info('Job Run Successfully!')
        p.wait_until_finish()
    except:
        logging.exception('Failed to launch datapipeline')
        raise    


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description=__doc__ , formatter_class=argparse.RawDescriptionHelpFormatter)
     run()
